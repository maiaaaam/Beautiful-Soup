import re
import requests
from api.fitness_api import get_calories_burned
from web_scraping.tasty_scraper import TastyScraper
from knowledge_base.flavor_graph import FlavorGraph
from models.sentiment_analyzer import ReviewSentimentAnalyzer
from models.topic_model import RecipeTopicModel
from api.fitness_api import get_workout_suggestions
from api.tasty_reviews import get_reviews
from api.nutrition_api import get_recipe_nutrition, get_nutrition_by_recipe_name
from api.recipe_api import get_recipe_spoonacular, get_recipe_tasty, get_recipe_mmabs, get_recipe_information, extract_ingredients, search_recipes_by_name
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our modules
# from api.workout_recommendation import WorkoutRecommender

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize our components
topic_model = RecipeTopicModel()
sentiment_analyzer = ReviewSentimentAnalyzer()
flavor_graph = FlavorGraph()
tasty_scraper = TastyScraper()
# workout_recommender = WorkoutRecommender()


try:
    topic_model.load_model()
    print("Topic model loaded successfully")
except:
    print("No pre-trained topic model found, will train on demand")

try:
    flavor_graph.load()
    print("Flavor graph loaded successfully")
except:
    print("No flavor graph found, will initialize empty graph")


@app.route('/api/recipes/spoonacular', methods=['GET'])
def get_recipes_spoonacular():
    """Get recipes based on ingredients"""
    ingredients = request.args.get('ingredients', '')
    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    ingredients_list = [ing.strip() for ing in ingredients.split(',')]
    recipes = get_recipe_spoonacular(ingredients_list)

    return jsonify(recipes)


@app.route('/api/recipes/tasty', methods=['GET'])
def get_recipes_tasty():
    """Get recipes based on ingredients"""
    ingredients = request.args.get('ingredients', '')
    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    ingredients_list = [ing.strip() for ing in ingredients.split(',')]
    recipes = get_recipe_tasty(ingredients_list)

    return jsonify(recipes)


@app.route('/api/recipes/mmabs', methods=['GET'])
def get_recipes_mmabs():
    """Get recipes based on ingredients"""
    ingredients = request.args.get('ingredients', '')
    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    ingredients_list = [ing.strip() for ing in ingredients.split(',')]
    recipes = get_recipe_mmabs(ingredients_list)

    return jsonify(recipes)


@app.route('/api/reviews', methods=['GET'])
def get_reviews_api():
    recipe = request.args.get('recipe')
    reviews = get_reviews(recipe)
    return jsonify(reviews)


@app.route('/api/recipes/search', methods=['GET'])
def search_recipe():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    results = search_recipes_by_name(query)
    return jsonify(results)


@app.route('/api/recipes/<recipe_id>/nutrition', methods=['GET'])
def get_nutrition(recipe_id):
    """Get nutrition information for a recipe"""
    nutrition = get_recipe_nutrition(recipe_id)
    if not nutrition:
        return jsonify({"error": "Nutrition information not found"}), 404

    return jsonify(nutrition)


@app.route('/api/recipes/<path:recipe_name>/nutrition', methods=['GET'])
def get_nutrition_by_path_name(recipe_name):
    # URL decode the recipe name
    recipe_name = requests.utils.unquote(recipe_name)

    # Get nutrition data
    nutrition_data = get_nutrition_by_recipe_name(recipe_name)

    # Return the data directly
    return jsonify(nutrition_data)


@app.route('/api/workout', methods=['GET'])
def get_workout_suggestions():
    calories = request.args.get('calories', default=300, type=int)
    tolerance = request.args.get('tolerance', default=50, type=int)

    # Use our API function to get workouts matching the calorie target
    activities = ["running", "walking",
                  "cycling", "swimming", "hiking", "yoga"]
    all_workouts = []

    # Collect workout options from different activities
    for activity in activities:
        workouts = get_calories_burned(activity)
        filtered_workouts = []

        for workout in workouts:
            # Check if the workout's calories are within our target range
            if calories - tolerance <= workout["total_calories"] <= calories + tolerance:
                # Add some additional useful information
                workout_data = {
                    # Extract main activity name
                    "activity": workout["name"].split(",")[0],
                    "duration_minutes": workout["duration_minutes"],
                    "estimated_calories": workout["total_calories"]
                }

                # Add activity-specific details when possible
                if "running" in workout["name"].lower():
                    pace_match = re.search(
                        r'(\d+(\.\d+)?) mph', workout["name"])
                    if pace_match:
                        speed = float(pace_match.group(1))
                        workout_data["pace"] = f"{speed} mph"
                        # Estimate distance based on speed and time
                        distance = (speed * workout["duration_minutes"]) / 60
                        workout_data["distance_km"] = round(
                            distance * 1.60934, 2)  # Convert miles to km

                elif "walking" in workout["name"].lower():
                    # Estimate steps (average 1300 steps per km, ~2100 per mile)
                    pace_match = re.search(
                        r'(\d+(\.\d+)?) mph', workout["name"])
                    if pace_match:
                        speed = float(pace_match.group(1))
                        distance_miles = (
                            speed * workout["duration_minutes"]) / 60
                        workout_data["steps"] = int(distance_miles * 2100)
                        workout_data["distance_km"] = round(
                            distance_miles * 1.60934, 2)

                filtered_workouts.append(workout_data)

        all_workouts.extend(filtered_workouts)

    # Sort by how close they are to the target calories
    all_workouts.sort(key=lambda x: abs(x["estimated_calories"] - calories))

    # Return top results
    return jsonify(all_workouts[:12])

# Endpoint to integrate with your recipe search/details flow


@app.route('/api/recipes/with-workouts', methods=['GET'])
def get_recipes_with_workouts():
    """Get recipes with workout recommendations"""
    ingredients = request.args.get('ingredients', '')
    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    ingredients_list = [ing.strip() for ing in ingredients.split(',')]
    recipes = get_recipe_spoonacular(ingredients_list)

    # Enhance recipes with workout recommendations
    enhanced_recipes = []
    for recipe in recipes:
        recipe_id = recipe.get("id")
        nutrition = get_recipe_nutrition(recipe_id)

        recipe_with_workout = recipe.copy()

        if nutrition and "calories" in nutrition:
            calories = nutrition.get("calories", 0)
            workout = workout_recommender.get_recommendation_for_meal(calories)
            recipe_with_workout["nutrition"] = nutrition
            recipe_with_workout["workout_recommendation"] = workout

        enhanced_recipes.append(recipe_with_workout)

    return jsonify(enhanced_recipes)


@app.route('/api/workout', methods=['GET'])
def workout_suggestions():
    """API endpoint to get workout suggestions based on calorie target"""
    try:
        calories = request.args.get('calories', 300)

        suggestions = get_workout_suggestions(calories)

        return jsonify(suggestions)
    except Exception as e:
        print(f"Error getting workout suggestions: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/recipes/similar', methods=['GET'])
def get_similar_recipes():
    """Get similar recipes based on topic modeling"""
    recipe_id = request.args.get('recipe_id', '')
    if not recipe_id:
        return jsonify({"error": "No recipe_id provided"}), 400

    # Check if model is trained
    if not topic_model.trained:
        return jsonify({"error": "Topic model not trained yet"}), 503

    similar_recipes = topic_model.get_similar_recipes(recipe_id)
    recipes_data = []

    for rid in similar_recipes:
        recipe = get_recipe_information(rid)
        if recipe:
            recipes_data.append({
                "id": recipe.get("id"),
                "title": recipe.get("title"),
                "image": recipe.get("image"),
                "readyInMinutes": recipe.get("readyInMinutes")
            })

    return jsonify(recipes_data)


@app.route('/api/flavor/suggestions', methods=['GET'])
def get_flavor_suggestions():
    """Get flavor pairing suggestions"""
    ingredients = request.args.get('ingredients', '')
    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    ingredients_list = [ing.strip() for ing in ingredients.split(',')]

    # Get ingredient IDs (this would depend on how you've set up your graph)
    # This is a simplification
    ingredient_ids = []
    for ing in ingredients_list:
        # Find the ingredient in the graph
        for node_id in flavor_graph.graph.nodes:
            if flavor_graph.graph.nodes[node_id]["name"].lower() == ing.lower():
                ingredient_ids.append(node_id)
                break

    suggestions = flavor_graph.suggest_missing_flavors(ingredient_ids)
    return jsonify(suggestions)


@app.route('/api/tasty/search', methods=['GET'])
def search_tasty():
    """Search for recipes on Tasty"""
    ingredients = request.args.get('ingredients', '')
    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    ingredients_list = [ing.strip() for ing in ingredients.split(',')]

    recipes = tasty_scraper.search_recipes(ingredients_list)
    return jsonify(recipes)


@app.route('/api/tasty/recipe', methods=['GET'])
def get_tasty_recipe():
    """Get detailed recipe information from Tasty"""
    url = request.args.get('url', '')
    if not url:
        return jsonify({"error": "No recipe URL provided"}), 400

    recipe = tasty_scraper.get_recipe_details(url)
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    # Analyze sentiment of reviews
    if recipe.get("reviews"):
        sentiment = sentiment_analyzer.analyze_reviews(recipe["reviews"])
        recipe["sentiment_analysis"] = sentiment

    return jsonify(recipe)


@app.route('/api/models/train', methods=['POST'])
def train_models():
    """Train the topic model with existing recipes"""
    data = request.json
    recipes = data.get("recipes", [])

    if not recipes:
        return jsonify({"error": "No recipes provided for training"}), 400

    try:
        # Train topic model
        recipe_topics = topic_model.train(recipes)
        topic_model.save_model()

        return jsonify({
            "status": "success",
            "message": "Models trained successfully",
            "recipe_count": len(recipes)
        })
    except Exception as e:
        return jsonify({"error": f"Training failed: {str(e)}"}), 500


@app.route('/api/slm/generate-recipe', methods=['POST'])
def generate_recipe():
    """Generate a recipe using a Small Language Model with ingredients"""
    data = request.json
    ingredients = data.get("ingredients", [])
    flavor_notes = data.get("flavor_notes", [])

    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    # This is a placeholder for integration with an SLM
    # You would need to implement the actual SLM integration
    recipe = {
        "title": f"Custom Recipe with {', '.join(ingredients[:3])}",
        "ingredients": [f"{ing}" for ing in ingredients],
        "instructions": [
            f"Prepare all ingredients: {', '.join(ingredients)}",
            "Combine ingredients in a suitable way.",
            "Cook until done.",
            "Serve and enjoy!"
        ],
        "notes": "This is a machine-generated recipe based on your ingredients."
    }

    return jsonify(recipe)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
