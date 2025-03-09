import requests
import os
from dotenv import load_dotenv

load_dotenv()

SPOONACULAR_API_KEY = "39d886d7dc594d7e91cfb2def05677bd"
BASE_URL = "https://api.spoonacular.com"

def get_recipe_nutrition(recipe_id):
    """
    Get nutrition information for a recipe
    """
    endpoint = f"{BASE_URL}/recipes/{recipe_id}/nutritionWidget.json"
    params = {
        "apiKey": SPOONACULAR_API_KEY
    }
    
    response = requests.get(endpoint, params=params)
    return response.json() if response.status_code == 200 else {}

def get_nutrition_by_recipe_name(recipe_name):
    """
    Search for a recipe by name and get its nutrition information
    """
    # First search for the recipe to get its ID
    endpoint = f"{BASE_URL}/recipes/complexSearch"
    search_params = {
        "apiKey": SPOONACULAR_API_KEY,
        "query": recipe_name,
        "number": 1  # Get just the top result
    }
    
    search_response = requests.get(endpoint, params=search_params)
    
    if search_response.status_code != 200 or not search_response.json().get("results"):
        return {"error": "Recipe not found"}
    
    # Get the ID of the first matching recipe
    recipe_id = search_response.json()["results"][0]["id"]
    
    # Then get nutrition info using the ID
    nutrition_endpoint = f"{BASE_URL}/recipes/{recipe_id}/nutritionWidget.json"
    nutrition_params = {
        "apiKey": SPOONACULAR_API_KEY
    }
    
    nutrition_response = requests.get(nutrition_endpoint, params=nutrition_params)
    
    if nutrition_response.status_code != 200:
        return {"error": "Failed to fetch nutrition data"}
    
    return nutrition_response.json()