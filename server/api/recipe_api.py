import requests
import os
from dotenv import load_dotenv
from api.utils import parse_spoonacular_response, get_recipe_nutrition, get_workouts
from api.env import SPOONACULAR_API_KEY, SPOONACULAR_BASE_URL
from api.tasty_recipe_list import scrape_recipes_tasty
from api.mmabs import build_recipe

load_dotenv()


"""
Recipe Format:
{
    name: recipe name,
    servings: servings (int),
    ingredients {
        name: quantity
    }
    instructions = []
}
"""


def get_recipe_spoonacular(ingredients, number=2):
    """
    Get recipes based on a list of ingredients
    """
    endpoint = f"{SPOONACULAR_BASE_URL}/recipes/findByIngredients"
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "ingredients": ",+".join(ingredients),
        "number": number,
    }
    response = requests.get(endpoint, params=params)

    recipes = parse_spoonacular_response(
        response.json()) if response.status_code == 200 else []
    nutrients = [get_recipe_nutrition(recipe) for recipe in recipes]
    workouts = [get_workouts(nutrient["Calories"]["amount"])
                for nutrient in nutrients]

    final_response = [{
        "recipe": recipes[i],
        "nutrients": nutrients[i],
        "workouts": workouts[i]
    } for i in range(len(recipes))]
    return final_response


def get_recipe_tasty(ingredients, number=2):
    tasty_response = scrape_recipes_tasty(ingredients, num_recipes=number)
    recipes = tasty_response["recipes"]
    urls = tasty_response["urls"]

    nutrients = [get_recipe_nutrition(recipe) for recipe in recipes]
    workouts = [get_workouts(nutrient["Calories"]["amount"])
                for nutrient in nutrients]

    modified_recipes = [{
        "recipe": recipes[i],
        "nutrients": nutrients[i],
        "workouts": workouts[i]
    } for i in range(len(recipes))]

    final_response = {
        "urls": urls,
        "recipes": modified_recipes
    }
    return final_response


def get_recipe_mmabs(ingredients):
    recipe = build_recipe(ingredients)
    nutrients = get_recipe_nutrition(recipe)
    final_response = {
        "recipe": recipe,
        "nutrients": nutrients,
        "workouts": get_workouts(nutrients["Calories"]["amount"])
    }
    return final_response


def get_recipe_information(recipe_id):
    """
    Get detailed information about a recipe including ingredients
    """
    endpoint = f"{SPOONACULAR_BASE_URL}/recipes/{recipe_id}/information"
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
    endpoint = f"{SPOONACULAR_BASE_URL}/recipes/complexSearch"
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
