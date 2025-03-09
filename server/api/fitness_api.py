import requests
import os
from dotenv import load_dotenv
 
load_dotenv()

# Using Nutritionix API for exercise data
NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID")
NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY")
BASE_URL = "https://trackapi.nutritionix.com/v2"

def get_workout_suggestions(calories):
    """
    Get workout suggestions based on calorie amount to burn
    """
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_API_KEY,
        "Content-Type": "application/json"
    }
    
    exercises = [
        {"query": "running", "duration": 20},
        {"query": "swimming", "duration": 30},
        {"query": "cycling", "duration": 30},
        {"query": "walking", "duration": 45},
        {"query": "yoga", "duration": 60}
    ]
    
    results = []
    for exercise in exercises:
        data = {
            "query": exercise["query"],
            "duration_min": exercise["duration"]
        }
        
        response = requests.post(
            f"{BASE_URL}/natural/exercise", 
            json=data, 
            headers=headers
        )
        
        if response.status_code == 200:
            exercise_data = response.json().get("exercises", [])
            if exercise_data:
                result = exercise_data[0]
                results.append({
                    "name": result.get("name"),
                    "duration": exercise["duration"],
                    "calories_burned": result.get("nf_calories"),
                    "met": result.get("met")
                })
    
    # Sort by efficiency (calories burned per minute)
    return sorted(
        results, 
        key=lambda x: x["calories_burned"] / x["duration"], 
        reverse=True
    )