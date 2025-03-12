import requests
import json
import time

SPOONACULAR_API_KEY = '9adc271ab4f247449672f16569ace989'
SPOONACULAR_URL = f'https://api.spoonacular.com/recipes/random?number=99&includeNutrition=false&apiKey={SPOONACULAR_API_KEY}'

iters = 200
all_recipes = {}

for i in range(iters):
    response = requests.get(SPOONACULAR_URL)
    if response.status_code == 200:
        recipes = response.json()['recipes']
        for recipe in recipes:
            all_recipes[recipe['id']] = recipe
        print(f"Completed iteration {i+1}/{iters}, size of all_recipes: {len(all_recipes)}")
    else:
        print(f"Failed to fetch recipes: {response.status_code}")
    time.sleep(2)

with open("all_recipes.json", "r") as infile:
    existing_recipes = json.load(infile)

all_recipes.update(existing_recipes)
with open("all_recipes.json", "w", encoding="utf-8") as outfile:
    json.dump(all_recipes, outfile, indent=2)