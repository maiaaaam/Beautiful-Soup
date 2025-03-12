from openai import OpenAI
import pandas as pd
import json

tastes = ['sweet', 'sour', 'salty', 'bitter',
          'umami', 'spicy', 'fatty', 'neutral']

client = OpenAI()


def get_tastes(ingredients: list[str]):
    """
    Takes a list of ingedients and returns the tastes of each ingredient.
    """
    prompt = (
        "The following is an available list of tastes:\n"
        f"{tastes}\n"
        "Can you annotate the following ingredients one-by-one with the appropriate tastes?\n"
        "The output format should be only the json with the key:str = ingredient name and value:list[str] = the applicable tastes. Give me only the json object and no text around it. Do not write the word 'json' in the beginning either.\n"
        f"{ingredients}\n"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
    except Exception as e:
        print("API call failed:", e)
        return {}

    taste_contents = response.choices[0].message.content.strip().replace(
        'json', '')

    try:
        # Parse the response into a Python dictionary
        return json.loads(taste_contents)
    except json.JSONDecodeError:
        print("Failed to parse JSON from ChatGPT response:")
        print(taste_contents)
        return {}


if __name__ == '__main__':
    node_url = "https://raw.githubusercontent.com/lamypark/FlavorGraph/master/input/nodes_191120.csv"
    nodes_df = pd.read_csv(node_url)
    ingredients_df = nodes_df[nodes_df['node_type'] == 'ingredient']
    ingredients = list(ingredients_df['name'])

    batch_size = 50
    taste_annotations = {}
    for i in range(0, len(ingredients), batch_size):
        last = min(i+batch_size, len(ingredients))
        ingredient_batch = ingredients[i:last]
        batch_tastes = get_tastes(ingredient_batch)
        taste_annotations.update(batch_tastes)
        print(f'Batch completed until {last} ingredients.')

    with open("taste_annotations.json", "w", encoding="utf-8") as outfile:
        json.dump(taste_annotations, outfile, indent=2)
