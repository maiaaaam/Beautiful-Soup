import json
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

model = ChatOllama(model="qwen2.5:3b", temperature=0)


def main():
    ingredients = ["chocolate", "butter", "sugar",
                   "vanilla", "orange", "milk"]
    ingredients_str = ', '.join(ingredients)
    prompt = f"Ingredients: {ingredients_str}."

    recipe_str = ""
    for chunk in model.stream([
        SystemMessage(
            """You are an expert chef. Using only the ingredient list given to you, create a detailed recipe with servings, quantities and instructions. You may use standard ingredients such as salt, pepper, sugar etc. as well if you need to.
            Important: Provide the response in a JSON format with the following keys: recipe_name, servings, ingredients(key=ingredient name, value=quantity), instructions."""),
        HumanMessage(prompt)
    ]):
        print(chunk.content, end="")
        recipe_str += chunk.content

    start_idx = recipe_str.find('{')
    end_idx = recipe_str.rfind('}') + 1
    recipe_json = json.loads(recipe_str[start_idx:end_idx])
    return recipe_json


if __name__ == "__main__":
    main()
