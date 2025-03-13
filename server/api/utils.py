import requests
from env import SPOONACULAR_API_KEY, SPOONACULAR_BASE_URL


def parse_spoonacular_response(response):
    recipes = []
    for recipe in response:
        name = recipe["title"]
        servings = 4
        ingredients = {
            ing["name"]: f"{ing['amount']} {ing['unit']}" for ing in recipe["usedIngredients"]}
        ingredients.update({
            ing["name"]: f"{ing['amount']} {ing['unit']}" for ing in recipe["missedIngredients"]})
        instructions = get_recipe_instructions(recipe["id"])
        recipes.append({"name": name, "servings": servings,
                       "ingredients": ingredients, "instructions": instructions})

    return recipes


def get_recipe_instructions(id):
    INSTRUCTIONS_URL = f"{SPOONACULAR_BASE_URL}/recipes/{id}/analyzedInstructions?apiKey={SPOONACULAR_API_KEY}"
    response = requests.get(INSTRUCTIONS_URL)
    return [step["step"] for step in response.json()[0]["steps"]]


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
