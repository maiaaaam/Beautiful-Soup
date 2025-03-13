import json
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage


model = ChatOllama(model="gemma3:1b-it-fp16", temperature=0)

# SYSTEM_PROMPT = """You are an expert chef. Using only the ingredient list given to you, create a detailed recipe with servings, quantities and instructions. You may use standard ingredients such as salt, pepper, sugar etc. as well if you need to.
# Important: Provide the response in a JSON format with the following keys: recipe_name, servings, ingredients(key=ingredient name, value=quantity), instructions."""
SYSTEM_PROMPT = """You are an expert chef. Using only the ingredient list given to you, create a detailed recipe with servings, quantities and instructions. You may use standard ingredients such as salt, pepper, sugar etc. as well if you need to.
Important: Provide only a JSON response of similar to the following sample example:
{
    "recipe_name": "Name for the recipe",
    "servings": serving size (int),
    "ingredients": {
        "ingredient 1": "quantity with units",
        "ingredient 2": "quantity with units",
        ...
    }
    "instructions": [
        "Step 1: ...",
        "Step 2: ...",
        ...
    ]
}"""


def generate_recipe(ingredients):
    ingredients = [ing.replace("_", " ") for ing in ingredients]
    ingredients_str = ', '.join(ingredients)
    prompt = f"Ingredients: {ingredients_str}."

    recipe_str = ""
    for chunk in model.stream([
        SystemMessage(SYSTEM_PROMPT),
        HumanMessage(prompt)
    ]):
        print(chunk.content, end="")
        recipe_str += chunk.content

    start_idx = recipe_str.find('{')
    end_idx = recipe_str.rfind('}') + 1
    recipe_json = json.loads(recipe_str[start_idx:end_idx])
    return recipe_json


if __name__ == "__main__":
    ingredients = ["strawberries", "avocado",
                   "honey", "lime", "black pepper", "yogurt"]
    generate_recipe(ingredients)
