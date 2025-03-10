import requests
import os
from dotenv import load_dotenv

load_dotenv()

SPOONACULAR_API_KEY = "API_KEY"
BASE_URL = "https://api.spoonacular.com"

def get_recipes_by_ingredients(ingredients, number=10):
    """
    Get recipes based on a list of ingredients
    """
    endpoint = f"{BASE_URL}/recipes/findByIngredients"
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "ingredients": ",".join(ingredients),
        "number": number,
        "ranking": 2 
    }
    
    response = requests.get(endpoint, params=params)
    return response.json() if response.status_code == 200 else []

def get_recipe_information(recipe_id):
    """
    Get detailed information about a recipe including ingredients
    """
    endpoint = f"{BASE_URL}/recipes/{recipe_id}/information"
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "includeNutrition": True
    }
    
    response = requests.get(endpoint, params=params)
    return response.json() if response.status_code == 200 else {}

def search_recipes_by_name(query, number=10):
    """
    Search for recipes by name
    """
    endpoint = f"{BASE_URL}/recipes/complexSearch"
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "query": query,
        "number": number,
        "addRecipeInformation": True,
        "fillIngredients": True
    }
    
    response = requests.get(endpoint, params=params)
    return response.json().get("results", []) if response.status_code == 200 else []

def extract_ingredients(recipe):
    """
    Extract ingredient information from a recipe
    """
    if not recipe or "extendedIngredients" not in recipe:
        return []
    
    return [
        {
            "id": ingredient.get("id"),
            "name": ingredient.get("name"),
            "amount": ingredient.get("amount"),
            "unit": ingredient.get("unit"),
            "original": ingredient.get("original")
        }
        for ingredient in recipe.get("extendedIngredients", [])
    ]
