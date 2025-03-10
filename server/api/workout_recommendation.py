# import requests
# import json
# import random
# from datetime import datetime, timedelta

# class WorkoutRecommender:
#     # def __init__(self):
#         # Typical calorie burn rates per minute for different activities
#         # self.activity_calorie_rates = {
#         #     "Run": 10,       # ~600 calories per hour
#         #     "Walk": 5,       # ~300 calories per hour
#         #     "Ride": 8,       # ~480 calories per hour
#         #     "Hike": 7,       # ~420 calories per hour
#         #     "Swim": 9,       # ~540 calories per hour
#         #     "WeightTraining": 6, # ~360 calories per hour
#         #     "Yoga": 4,       # ~240 calories per hour
#         # }
        
#         # # Default pace values (in minutes per km) for different activities
#         # self.default_pace = {
#         #     "Run": 6,        # 6 min/km
#         #     "Walk": 12,      # 12 min/km
#         #     "Ride": 3,       # 3 min/km (20 km/h)
#         #     "Hike": 15,      # 15 min/km
#         #     "Swim": 2        # 2 min/100m
#         # }
        
#         # # Sample step counts per km for different activities
#         # self.steps_per_km = {
#         #     "Run": 1200,     # ~1200 steps per km
#         #     "Walk": 1300,    # ~1300 steps per km
#         #     "Hike": 1300     # ~1300 steps per km
#         # }
    
#     def get_workout_suggestions(target_calories, user_preferences=None):
#         """
#         Get workout suggestions based on calorie target and user preferences
        
#         Args:
#             target_calories (int/float): Calories to burn
#             user_preferences (dict): Optional user preferences
            
#         Returns:
#             list: List of workout suggestions
#         """
#         # Convert target_calories to a float if it's a string
#         try:
#             target_calories = float(target_calories)
#         except (ValueError, TypeError):
#             target_calories = 0  # Default value
        
#         # Default workouts with estimated calorie burn rates (calories per minute)
#         # default_workouts = {
#         #     "Running": 10,       # ~600 calories per hour
#         #     "Cycling": 8,        # ~480 calories per hour  
#         #     "Swimming": 9,       # ~540 calories per hour
#         #     "Walking": 5,        # ~300 calories per hour
#         #     "Hiking": 7,         # ~420 calories per hour
#         #     "Yoga": 4,           # ~240 calories per hour
#         #     "Weight Training": 6 # ~360 calories per hour
#         # }
        
#         # # Default pace values (in minutes per km) for different activities
#         # default_pace = {
#         #     "Running": 6,        # 6 min/km
#         #     "Walking": 12,      # 12 min/km
#         #     "Cycling": 3,       # 3 min/km (20 km/h)
#         #     "Hiking": 15,      # 15 min/km
#         #     "Swimming": 2        # 2 min/100m (for 100m segments)
#         # }
        
#         # # Sample step counts per km for different activities
#         # steps_per_km = {
#         #     "Running": 1200,     # ~1200 steps per km
#         #     "Walking": 1300,    # ~1300 steps per km
#         #     "Hiking": 1300     # ~1300 steps per km
#         # }
        
#         suggestions = []
        
#         # Generate workout suggestions for each activity
#         for activity, rate in default_workouts.items():
#             # Calculate duration needed to burn target calories
#             duration_minutes = round(target_calories / rate)
            
#             # Skip if duration is unreasonably long (over 3 hours)
#             if duration_minutes > 180:
#                 continue
            
#             # Create base suggestion
#             suggestion = {
#                 "activity": activity,
#                 "duration_minutes": duration_minutes,
#                 "estimated_calories": int(target_calories)
#             }
            
#             # Add distance, pace and steps if applicable
#             if activity in default_pace:
#                 # Calculate approximate distance in km
#                 hours = duration_minutes / 60
                
#                 if activity == "Swimming":
#                     # Swimming is typically measured in 100m increments
#                     distance = hours * 60 / default_pace[activity] * 10  # in km
#                     suggestion["pace"] = f"{default_pace[activity]} min/100m"
#                 else:
#                     # Calculate how far you can go in the given time at the default pace
#                     distance = hours * 60 / default_pace[activity]  # in km
#                     suggestion["pace"] = f"{default_pace[activity]} min/km"
                
#                 suggestion["distance_km"] = round(distance, 2)
                
#                 # Add step count for relevant activities
#                 if activity in steps_per_km:
#                     suggestion["steps"] = round(distance * steps_per_km[activity])
            
#             suggestions.append(suggestion)
        
#         # Sort by duration (shorter workouts first)
#         suggestions.sort(key=lambda x: x["duration_minutes"])
        
#         return suggestions
    
#     def _analyze_strava_data(self, activities):
#         """
#         Analyze Strava activities to personalize calorie burn rates
        
#         Args:
#             activities (list): List of Strava activities
            
#         Returns:
#             dict: Dictionary of personalized calorie burn rates
#         """
#         activity_stats = {}
        
#         for activity in activities:
#             activity_type = activity.get("type")
#             if not activity_type:
#                 continue
                
#             calories = activity.get("calories", 0)
#             moving_time = activity.get("moving_time", 0)  # in seconds
            
#             if calories <= 0 or moving_time <= 0:
#                 continue
                
#             # Calculate calories per minute
#             calories_per_minute = (calories / (moving_time / 60))
            
#             if activity_type not in activity_stats:
#                 activity_stats[activity_type] = {"total_calories": 0, "total_minutes": 0}
                
#             activity_stats[activity_type]["total_calories"] += calories
#             activity_stats[activity_type]["total_minutes"] += (moving_time / 60)
        
#         # Calculate average calories per minute for each activity type
#         personalized_rates = {}
#         for activity_type, stats in activity_stats.items():
#             if stats["total_minutes"] > 0:
#                 personalized_rates[activity_type] = round(stats["total_calories"] / stats["total_minutes"], 1)
        
#         return personalized_rates
    
#     def get_recommendation_for_meal(self, meal_calories, user_preferences=None):
#         """
#         Get workout recommendation based on meal calories
        
#         Args:
#             meal_calories (float): Calories in the meal
#             user_preferences (dict): Optional user preferences
            
#         Returns:
#             dict: Recommended workout
#         """
#         # Typically recommend burning 50-75% of meal calories
#         target_calories = meal_calories * 0.6
        
#         suggestions = self.get_workout_suggestions(target_calories)
        
#         # If user has preferences, sort suggestions accordingly
#         if user_preferences and "preferred_activities" in user_preferences:
#             preferred = user_preferences["preferred_activities"]
#             suggestions.sort(key=lambda x: preferred.index(x["activity"]) if x["activity"] in preferred else 999)
        
#         # Return top suggestion
#         return suggestions[0] if suggestions else None