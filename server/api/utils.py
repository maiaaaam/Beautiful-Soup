import requests
from urllib.parse import urlencode
import json
import re

from api.env import SPOONACULAR_API_KEY, SPOONACULAR_BASE_URL


def extract_number(text):
    if type(text) != str:
        return text

    pattern = r'\d+'
    match = re.search(pattern, text)
    if match:
        return int(match.group())
    else:
        return None


def parse_spoonacular_response(response):
    recipes = []
    for recipe in response:
        name = recipe["title"]
        servings = 4
        ingredients = [
            f"{ing['name']} {ing['amount']} {ing['unit']}" for ing in recipe["usedIngredients"]]
        ingredients.extend(
            [f"{ing['name']} {ing['amount']} {ing['unit']}" for ing in recipe["missedIngredients"]])
        instructions = get_recipe_instructions(recipe["id"])
        recipes.append({"name": name, "servings": servings,
                       "ingredients": ingredients, "instructions": instructions})

    return recipes


def get_recipe_instructions(id):
    INSTRUCTIONS_URL = f"{SPOONACULAR_BASE_URL}/recipes/{id}/analyzedInstructions?apiKey={SPOONACULAR_API_KEY}"
    response = requests.get(INSTRUCTIONS_URL)
    return [step["step"] for step in response.json()[0]["steps"]]


def get_macros(nutrients_list):
    macros = {}

    for item in nutrients_list:
        for nutrient in item:
            name = nutrient['name']

            if name not in macros:
                macros[name] = {
                    'name': name,
                    'amount': 0,
                    'unit': nutrient['unit']
                }

            macros[name]['amount'] += nutrient['amount']
            macros[name]['amount'] = round(macros[name]['amount'], 3)

    return macros


def get_recipe_nutrition(recipe):
    NUTRITION_URL = f"{SPOONACULAR_BASE_URL}/recipes/parseIngredients?apiKey={SPOONACULAR_API_KEY}"

    recipe_ingredients = "\n".join(recipe["ingredients"])
    params = {"servings": extract_number(recipe["servings"]),
              "ingredientList": recipe_ingredients, "includeNutrition": True}
    payload = urlencode(params)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(NUTRITION_URL, headers=headers, data=payload)
    macros = get_macros([ing['nutrition']['nutrients']
                         for ing in json.loads(response.text) if "nutrition" in ing])
    important_macro_types = [
        'Protein', 'Carbohydrates', 'Fat',
        'Saturated Fat', 'Mono Unsaturated Fat', 'Poly Unsaturated Fat',
        'Cholesterol', 'Fiber', 'Sugar',
        'Sodium', 'Potassium', 'Calcium', 'Iron',
        'Vitamin A', 'Vitamin C', 'Vitamin D', 'Vitamin B12', 'Calories'
    ]

    important_macros = {macro: macros[macro]
                        for macro in important_macro_types}
    return important_macros


if __name__ == "__main__":
    ingredients = ["egg", "sugar", "butter"]
    endpoint = f"{SPOONACULAR_BASE_URL}/recipes/findByIngredients"
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "ingredients": ",+".join(ingredients),
        "number": 2,
    }
    response = requests.get(endpoint, params=params)
    recipes = parse_spoonacular_response(response.json())
    x = 1
