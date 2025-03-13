from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

# given a list of ingredients, go to tasty and get the recipes of the first 3 igredients

def setup_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    return webdriver.Chrome(options=chrome_options)


def scrape_tasty_links(ingredients):
    search_query = '+'.join(ingredients)
    url = f"https://tasty.co/search?q={search_query}&sort=popular"

    driver = setup_chrome_driver()

    try:
        print(f"Navigating to: {url}")
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "li.feed-item")))

        # add delay to ensure all content is loaded
        time.sleep(2)

        feed_items = driver.find_elements(By.CSS_SELECTOR, "li.feed-item")
        recipe_links = []

        for item in feed_items:
            try:
                a_tag = item.find_element(By.TAG_NAME, "a")
                href = a_tag.get_attribute("href")
                recipe_links.append(href)
            except Exception as e:
                print(f"Error extracting link from feed item: {e}")

        print(f"Found {len(recipe_links)} recipe links")
        return recipe_links

    finally:
        driver.quit()


def scrape_recipe_details(url, driver, wait):
    print(f"Scraping recipe: {url}")
    driver.get(url)

    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "h1.recipe-name")))

    # add delay to ensure all content is loaded
    time.sleep(2)

    recipe_details = {
        "url": url,
        "name": "",
        "servings": "",
        "ingredients": [],
        "preparation_steps": []
    }

    try:
        recipe_name = driver.find_element(
            By.CSS_SELECTOR, "h1.recipe-name").text
        recipe_details["name"] = recipe_name
        print(f"Recipe name: {recipe_name}")
    except Exception as e:
        print(f"Error getting recipe name: {e}")

    try:
        # get servings
        servings = driver.find_element(
            By.CSS_SELECTOR, "p.servings-display").text
        recipe_details["servings"] = servings
        print(f"Servings: {servings}")
    except Exception as e:
        print(f"Error getting servings: {e}")

    try:
        # get ingredients
        ingredient_elements = driver.find_elements(
            By.CSS_SELECTOR, "li.ingredient")
        ingredients = [element.text for element in ingredient_elements]
        recipe_details["ingredients"] = ingredients
        print(f"Found {len(ingredients)} ingredients")
    except Exception as e:
        print(f"Error getting ingredients: {e}")

    try:
        # get preparation steps
        prep_steps_ol = driver.find_element(By.CSS_SELECTOR, "ol.prep-steps")
        step_elements = prep_steps_ol.find_elements(By.TAG_NAME, "li")
        steps = [element.text for element in step_elements]
        recipe_details["preparation_steps"] = steps
        print(f"Found {len(steps)} preparation steps")
    except Exception as e:
        print(f"Error getting preparation steps: {e}")

    return recipe_details


def scrape_recipes(ingredients, num_recipes=3):
    # get the recipe links
    recipe_links = scrape_tasty_links(ingredients)

    if not recipe_links:
        print("No recipe links found.")
        return []

    driver = setup_chrome_driver()
    wait = WebDriverWait(driver, 10)

    recipes = []

    try:
        # limit to the first num_recipes
        links_to_scrape = recipe_links[:num_recipes]
        print(f"Scraping details for {len(links_to_scrape)} recipes")

        for url in links_to_scrape:
            recipe_details = scrape_recipe_details(url, driver, wait)
            recipes.append(recipe_details)

            # add a delay between requests
            time.sleep(2)

        return recipe_links, recipes

    finally:
        driver.quit()


available_ingredients = ['lemon', 'butter', 'sugar']
recipe_links, recipes = scrape_recipes(available_ingredients, num_recipes=3)

print(json.dumps(recipes, indent=2))
