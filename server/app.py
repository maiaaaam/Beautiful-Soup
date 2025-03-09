from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our modules
from api.recipe_api import get_recipes_by_ingredients, get_recipe_information, extract_ingredients, search_recipes_by_name
from api.nutrition_api import get_recipe_nutrition, get_nutrition_by_recipe_name
from api.fitness_api import get_workout_suggestions
from models.topic_model import RecipeTopicModel
from models.sentiment_analyzer import ReviewSentimentAnalyzer
from knowledge_base.flavor_graph import FlavorGraph
from web_scraping.tasty_scraper import TastyScraper
import requests

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize our components
topic_model = RecipeTopicModel()
sentiment_analyzer = ReviewSentimentAnalyzer()
flavor_graph = FlavorGraph()
tasty_scraper = TastyScraper()

# Try to load pre-trained models if available
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

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Get recipes based on ingredients"""
    ingredients = request.args.get('ingredients', '')
    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400
        
    ingredients_list = [ing.strip() for ing in ingredients.split(',')]
    recipes = get_recipes_by_ingredients(ingredients_list)
    
    return jsonify(recipes)

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
def get_workout():
    """Get workout suggestions based on calories"""
    calories = request.args.get('calories', 0)
    try:
        calories = float(calories)
    except ValueError:
        return jsonify({"error": "Invalid calorie value"}), 400
        
    workout = get_workout_suggestions(calories)
    return jsonify(workout)

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