from textblob import TextBlob
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class ReviewSentimentAnalyzer:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
    def preprocess_text(self, text):
        """
        Clean and preprocess review text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stop words and lemmatize
        tokens = [
            self.lemmatizer.lemmatize(word) 
            for word in tokens 
            if word not in self.stop_words
        ]
        
        return ' '.join(tokens)
    
    def analyze_sentiment(self, review_text):
        """
        Analyze the sentiment of a review
        """
        processed_text = self.preprocess_text(review_text)
        blob = TextBlob(processed_text)
        
        # Get polarity score (-1 to 1)
        polarity = blob.sentiment.polarity
        
        # Map to sentiment category
        if polarity > 0.3:
            sentiment = "positive"
        elif polarity < -0.3:
            sentiment = "negative"
        else:
            sentiment = "neutral"
            
        return {
            "polarity": polarity,
            "sentiment": sentiment,
            "subjectivity": blob.sentiment.subjectivity
        }
    
    def analyze_reviews(self, reviews):
        """
        Analyze multiple reviews and provide summary
        """
        if not reviews:
            return {
                "overall_sentiment": "Unknown",
                "positive_percentage": 0,
                "negative_percentage": 0,
                "neutral_percentage": 0,
                "review_count": 0,
                "analyzed_reviews": []
            }
            
        analyzed = []
        sentiments = {"positive": 0, "negative": 0, "neutral": 0}
        
        for review in reviews:
            review_text = review.get("text", "")
            result = self.analyze_sentiment(review_text)
            
            analyzed.append({
                "text": review_text,
                "sentiment": result["sentiment"],
                "polarity": result["polarity"],
                "subjectivity": result["subjectivity"]
            })
            
            sentiments[result["sentiment"]] += 1
            
        total = len(reviews)
        
        return {
            "overall_sentiment": max(sentiments, key=sentiments.get),
            "positive_percentage": (sentiments["positive"] / total) * 100,
            "negative_percentage": (sentiments["negative"] / total) * 100,
            "neutral_percentage": (sentiments["neutral"] / total) * 100,
            "review_count": total,
            "analyzed_reviews": analyzed
        }