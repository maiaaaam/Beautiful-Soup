import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID")
NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY")

# Application Settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
PORT = int(os.getenv("PORT", 5000))
HOST = os.getenv("HOST", "0.0.0.0")

# Paths
MODEL_PATH = os.getenv("MODEL_PATH", "models")
KNOWLEDGE_BASE_PATH = os.getenv("KNOWLEDGE_BASE_PATH", "knowledge_base")

# Cache settings
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True").lower() == "true"
CACHE_TIMEOUT = int(os.getenv("CACHE_TIMEOUT", 3600))  # 1 hour default

# Web scraping settings
SCRAPING_DELAY = float(os.getenv("SCRAPING_DELAY", 1.5))  # seconds