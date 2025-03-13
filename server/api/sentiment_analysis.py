import pandas as pd
from nltk import pos_tag
from nltk.corpus import sentiwordnet as swn
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import RegexpTokenizer, word_tokenize
import liwc
from textblob import TextBlob

parse, category_names = liwc.load_token_parser('api/data/liwc.dic')


def get_sentiwordnet_score(text):
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    score = 0
    count = 0

    for word, tag in tagged:
        if tag.startswith('J'):  # adjective
            synsets = list(swn.senti_synsets(word, 'a'))
        elif tag.startswith('V'):  # verb
            synsets = list(swn.senti_synsets(word, 'v'))
        elif tag.startswith('N'):  # noun
            synsets = list(swn.senti_synsets(word, 'n'))
        elif tag.startswith('R'):  # adverb
            synsets = list(swn.senti_synsets(word, 'r'))
        else:
            synsets = []

        if synsets:
            word_score = synsets[0].pos_score() - synsets[0].neg_score()
            score += word_score
            count += 1

    return score / count if count > 0 else 0


def get_liwc_score(text):
    tokenizer = RegexpTokenizer(r'\b\w+\b')
    words = tokenizer.tokenize(text.lower())

    posemo_count = 0
    negemo_count = 0

    for word in words:
        categories = parse(word)

        if 'posemo' in categories:
            posemo_count += 1
        if 'negemo' in categories:
            negemo_count += 1

    count = posemo_count + negemo_count

    return (posemo_count - negemo_count) / count if count > 0 else 0


def perform_sentiment_analysis(reviews):
    reviews_df = pd.DataFrame({'review': reviews})
    methods = ['VADER', 'TextBlob', 'SentiWordNet', 'LIWC', 'Combined']

    # method 1: VADER
    vader = SentimentIntensityAnalyzer()
    reviews_df['VADER'] = reviews_df['review'].apply(
        lambda x: vader.polarity_scores(x)['compound'])

    # method 2: TextBlob
    reviews_df['TextBlob'] = reviews_df['review'].apply(
        lambda x: TextBlob(x).sentiment.polarity)

    # method 3: SentiWordNet
    reviews_df['SentiWordNet'] = reviews_df['review'].apply(
        get_sentiwordnet_score)

    # method 4: LIWC
    reviews_df['LIWC'] = reviews_df['review'].apply(get_liwc_score)
    # normalize and averaging the scores
    for col in ['VADER', 'TextBlob', 'SentiWordNet', 'LIWC']:
        max_val = reviews_df[col].abs().max()
        if max_val > 0:
            reviews_df[col] = reviews_df[col] / max_val

    reviews_df['Combined'] = (reviews_df['VADER'] + reviews_df['TextBlob'] +
                              reviews_df['SentiWordNet'] + reviews_df['LIWC']) / 4

    return {
        "reviews": list(reviews_df['review']),
        "score": list(reviews_df['Combined'])
    }
