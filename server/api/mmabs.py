import pandas as pd
import numpy as np
from collections import Counter, defaultdict
from api.generate import generate_recipe

nodes_df = pd.read_csv("api/data/nodes.csv")
edges_df = pd.read_csv("api/data/edges.csv")

complementary_map = {
    'sweet': ['sour', 'bitter', 'salty', 'spicy'],
    'sour': ['sweet', 'fatty', 'salty'],
    'bitter': ['sweet', 'fatty', 'umami'],
    'salty': ['sweet', 'fatty', 'sour'],
    'umami': ['bitter', 'fresh', 'citrusy'],
    'fatty': ['sour', 'fresh', 'spicy'],
    'spicy': ['sweet', 'fatty', 'fresh'],
    'slightly sweet': ['sour', 'bitter', 'salty', 'spicy'],
    'tangy': ['sweet', 'fatty', 'umami'],
    'tart': ['sweet', 'fatty', 'umami'],
    'citrusy': ['umami', 'sweet', 'earthy'],
    'earthy': ['citrusy', 'fresh', 'spicy'],
    'smoky': ['sweet', 'fresh', 'tangy']
}


def recommend_ingredients(input_ingredients, nodes_df, edges_df, top_n=5):
    input_ids = []

    # obtain ingredients nodes from the graph
    for ingredient in input_ingredients:
        matched = nodes_df[nodes_df['name'].str.lower() == ingredient.lower()]
        input_ids.append(matched.iloc[0]['node_id'])

    if not input_ids:
        return pd.DataFrame(columns=['name', 'score', 'flavor_profiles', 'reason'])

    # obtain flavor profiles of input ingredients
    input_flavors = []
    for id in input_ids:
        ingredient_data = nodes_df[nodes_df['node_id'] == id]
        flavors = ingredient_data['flavours'].iloc[0]
        input_flavors.extend(flavors)

    flavor_counts = Counter(input_flavors)

    # find which flavors are missing or underrepresented
    missing_flavors = []
    for flavor in input_flavors:
        if flavor in complementary_map:
            for complement in complementary_map[flavor]:
                if complement not in flavor_counts or flavor_counts[complement] < flavor_counts[flavor]:
                    missing_flavors.append(complement)

    # add base flavors if dish is too one-dimensional
    if len(set(input_flavors)) <= 2:
        missing_flavors.extend(['umami', 'salty'])

    missing_flavor_counts = Counter(missing_flavors)

    # find ingredients that pair well with input ingredients
    candidate_scores = {}

    for input_id in input_ids:
        pairs = edges_df[(edges_df['id_1'] == input_id) |
                         (edges_df['id_2'] == input_id)]

        for _, row in pairs.iterrows():
            other_id = row['id_2'] if row['id_1'] == input_id else row['id_1']
            if other_id not in input_ids:  # dont recommend ingredients already in input
                if other_id not in candidate_scores:
                    candidate_scores[other_id] = {'score': 0, 'count': 0}
                candidate_scores[other_id]['score'] += row['score']
                candidate_scores[other_id]['count'] += 1

    # calculate average score for each candidate
    for candidate_id in candidate_scores:
        candidate_scores[candidate_id]['avg_score'] = (
            candidate_scores[candidate_id]['score'] /
            candidate_scores[candidate_id]['count']
        )

    # score candidates based on pairing strength and flavor complementarity
    final_candidates = []

    for candidate_id, score_data in candidate_scores.items():
        # get candidate data from nodes_df
        candidate_data = nodes_df[nodes_df['node_id'] == candidate_id]

        if len(candidate_data) == 0:
            continue

        candidate_data = candidate_data.iloc[0]
        candidate_name = candidate_data['name']
        candidate_flavors = candidate_data['flavours']

        # calculate flavor complementarity score
        flavor_complement_score = sum(
            missing_flavor_counts[flavor] for flavor in candidate_flavors if flavor in missing_flavor_counts)

        # using linear combination of score and complementarity to obtain the final score
        final_score = score_data['avg_score'] * \
            (1 + 0.5 * flavor_complement_score)

        # add reason for recommendation
        matching_flavors = set(candidate_flavors).intersection(missing_flavors)
        if matching_flavors:
            flavor_reason = f"Adds {', '.join(matching_flavors)} to balance the dish"
        else:
            flavor_reason = "Pairs well with existing ingredients"

        final_candidates.append({
            'id': candidate_id,
            'name': candidate_name,
            'score': final_score,
            'flavor_profiles': ', '.join(candidate_flavors),
            'reason': flavor_reason
        })

    # Sort by score and return top recommendations
    recommendations = pd.DataFrame(final_candidates)
    if len(recommendations) > 0:
        recommendations = recommendations.sort_values(
            'score', ascending=False).head(top_n)
        recommendations = recommendations[[
            'name', 'score', 'flavor_profiles', 'reason']]

    return recommendations

# defining helper softmax to create a probability distribution


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def build_ingredient_list(initial_ingredients, nodes_df, edges_df, k=5, top_n=5, temperature=1.0):
    """
    - We build the ingredient list auto-regressively (like how LLMs generate words)
    - Thus we have similar parameters such as LLMs i.e. top_n and temperature
    - They control the randomness of recipe generation
    """
    if not initial_ingredients:
        return [], {"error": "No initial ingredients provided"}

    current_ingredients = initial_ingredients.copy()
    if len(current_ingredients) >= k:
        return current_ingredients, {"info": f"Already have {len(current_ingredients)} ingredients, no need to add more"}

    # just for tracking
    process_log = {}

    iteration = 1
    while len(current_ingredients) < k:
        recommendations = recommend_ingredients(
            current_ingredients, nodes_df, edges_df, top_n=top_n)

        if len(recommendations) == 0:
            process_log[f"iteration_{iteration}"] = {
                "error": "No recommendations found",
                "current_ingredients": current_ingredients
            }
            break

        # get scores and create softmax distribution
        scores = recommendations['score'].values
        scaled_scores = scores / temperature
        probabilities = softmax(scaled_scores)

        selected_idx = np.random.choice(len(recommendations), p=probabilities)
        selected_recommendation = recommendations.iloc[selected_idx]
        new_ingredient = selected_recommendation['name']

        # log this iteration with all candidates and their probabilities
        candidates_info = []
        for i, (_, rec) in enumerate(recommendations.iterrows()):
            candidates_info.append({
                "name": rec['name'],
                "score": rec['score'],
                "probability": probabilities[i],
                "selected": (i == selected_idx)
            })

        process_log[f"iteration_{iteration}"] = {
            "current_ingredients": current_ingredients.copy(),
            "added_ingredient": new_ingredient,
            "reason": selected_recommendation['reason'],
            "flavor_profiles": selected_recommendation['flavor_profiles'],
            "selection_probability": probabilities[selected_idx],
            "all_candidates": candidates_info
        }

        current_ingredients.append(new_ingredient)
        iteration += 1

    return current_ingredients, process_log


def build_recipe(ingredients):
    ingredients = [ing.replace(" ", "_") for ing in ingredients]
    final_ingredients, _ = build_ingredient_list(
        ingredients, nodes_df, edges_df, k=6, top_n=10)

    return generate_recipe(final_ingredients)
