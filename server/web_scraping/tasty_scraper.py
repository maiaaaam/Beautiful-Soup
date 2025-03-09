import requests
from bs4 import BeautifulSoup
import json
import time
import random

class TastyScraper:
    def __init__(self):
        self.base_url = "https://tasty.co"
        self.search_url = f"{self.base_url}/search"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.recipe_cache = {}
        
    def search_recipes(self, ingredients, max_recipes=10):
        """
        Search for recipes on Tasty based on ingredients
        """
        query = " ".join(ingredients)
        params = {
            "q": query,
            "type": "recipe"
        }
        
        try:
            response = requests.get(self.search_url, params=params, headers=self.headers)
            if response.status_code != 200:
                print(f"Error searching Tasty: {response.status_code}")
                return []
                
            soup = BeautifulSoup(response.text, 'html.parser')
            recipe_cards = soup.select('.feed-item')
            
            results = []
            for card in recipe_cards[:max_recipes]:
                link_elem = card.select_one('a')
                if not link_elem:
                    continue
                    
                recipe_url = link_elem.get('href')
                if not recipe_url.startswith('http'):
                    recipe_url = f"{self.base_url}{recipe_url}"
                    
                title_elem = card.select_one('.feed-item__title')
                title = title_elem.text.strip() if title_elem else "Unknown Recipe"
                
                img_elem = card.select_one('img')
                img_url = img_elem.get('src') if img_elem else None
                
                results.append({
                    "title": title,
                    "url": recipe_url,
                    "image_url": img_url
                })
                
            return results
            
        except Exception as e:
            print(f"Error scraping Tasty search: {str(e)}")
            return []
    
    def get_recipe_details(self, recipe_url):
        """
        Get detailed information about a recipe
        """
        # Check cache first
        if recipe_url in self.recipe_cache:
            return self.recipe_cache[recipe_url]
            
        try:
            # Add a small delay to be respectful to the website
            time.sleep(random.uniform(1, 3))
            
            response = requests.get(recipe_url, headers=self.headers)
            if response.status_code != 200:
                print(f"Error fetching recipe: {response.status_code}")
                return None
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract recipe data
            title = soup.select_one('h1').text.strip() if soup.select_one('h1') else "Unknown Recipe"
            
            # Get ingredients
            ingredient_elems = soup.select('.ingredients__section li')
            ingredients = [elem.text.strip() for elem in ingredient_elems]
            
            # Get instructions
            instruction_elems = soup.select('.preparation__step')
            instructions = [elem.text.strip() for elem in instruction_elems]
            
            # Get reviews
            review_elems = soup.select('.reviews-feed__item')
            reviews = []
            
            for review in review_elems:
                author_elem = review.select_one('.comment-author')
                content_elem = review.select_one('.comment-text')
                date_elem = review.select_one('.comment-meta')
                
                if content_elem:
                    reviews.append({
                        "author": author_elem.text.strip() if author_elem else "Anonymous",
                        "text": content_elem.text.strip(),
                        "date": date_elem.text.strip() if date_elem else "Unknown date"
                    })
            
            recipe_data = {
                "title": title,
                "url": recipe_url,
                "ingredients": ingredients,
                "instructions": instructions,
                "reviews": reviews
            }
            
            # Cache the result
            self.recipe_cache[recipe_url] = recipe_data
            
            return recipe_data
            
        except Exception as e:
            print(f"Error scraping recipe details: {str(e)}")
            return None