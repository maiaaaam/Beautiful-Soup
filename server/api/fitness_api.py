import requests
import re

# API credentials
CALORIESBURNED_API_KEY = "boJKzaMmlnmBxVsHsWs7kA==CTIsE9cu29CZLqPD"
BASE_URL = "https://api.api-ninjas.com/v1/caloriesburned"

def get_calories_burned(activity):
    """
    Get calories burned for a specific activity
    """
    params = {
        "activity": activity
    }
    
    headers = {
        "X-Api-Key": CALORIESBURNED_API_KEY
    }
    
    response = requests.get(BASE_URL, params=params, headers=headers)
    return response.json() if response.status_code == 200 else []

def get_workout_suggestions(calories, tolerance=50):
    """
    Get workout suggestions based on calorie target
    """
    # List of activities to search
    activities = ["running", "walking", "cycling", "swimming", "hiking", "yoga"]
    all_workouts = []
    
    # Collect workout options from different activities
    for activity in activities:
        workouts = get_calories_burned(activity)
        filtered_workouts = []
        
        for workout in workouts:
            # Check if the workout's calories are within our target range
            if calories - tolerance <= workout["total_calories"] <= calories + tolerance:
                # Add some additional useful information
                workout_data = {
                    "activity": workout["name"].split(",")[0],  # Extract main activity name
                    "duration_minutes": workout["duration_minutes"],
                    "estimated_calories": workout["total_calories"]
                }
                
                # Add activity-specific details when possible
                if "running" in workout["name"].lower():
                    pace_match = re.search(r'(\d+(\.\d+)?) mph', workout["name"])
                    if pace_match:
                        speed = float(pace_match.group(1))
                        workout_data["pace"] = f"{speed} mph"
                        # Estimate distance based on speed and time
                        distance = (speed * workout["duration_minutes"]) / 60
                        workout_data["distance_km"] = round(distance * 1.60934, 2)  # Convert miles to km
                
                elif "walking" in workout["name"].lower():
                    # Estimate steps (average 1300 steps per km, ~2100 per mile)
                    pace_match = re.search(r'(\d+(\.\d+)?) mph', workout["name"])
                    if pace_match:
                        speed = float(pace_match.group(1))
                        distance_miles = (speed * workout["duration_minutes"]) / 60
                        workout_data["steps"] = int(distance_miles * 2100)
                        workout_data["distance_km"] = round(distance_miles * 1.60934, 2)
                
                filtered_workouts.append(workout_data)
        
        all_workouts.extend(filtered_workouts)
    
    # Sort by how close they are to the target calories
    all_workouts.sort(key=lambda x: abs(x["estimated_calories"] - calories))
    
    # Return top results
    return all_workouts[:12]