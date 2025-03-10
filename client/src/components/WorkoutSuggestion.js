// import React, { useState } from 'react';
// import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

// const WorkoutRecommendations = () => {
//   const [caloriesInput, setCaloriesInput] = useState(375);
//   const [workouts, setWorkouts] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);

//   const fetchWorkoutSuggestions = async () => {
//     setLoading(true);
//     setError(null);
    
//     try {
//       const response = await fetch(`http://localhost:5000/api/workout?calories=${caloriesInput}`);
//       if (!response.ok) {
//         throw new Error('Failed to fetch workout suggestions');
//       }
      
//       const data = await response.json();
//       setWorkouts(data);
//     } catch (err) {
//       setError(err.message);
//       console.error('Error fetching workouts:', err);
//     } finally {
//       setLoading(false);
//     }
//   };

//   // Activity icons for visual representation
//   const activityIcons = {
//     Run: '🏃',
//     Walk: '🚶',
//     Ride: '🚴',
//     Swim: '🏊',
//     Hike: '🥾',
//     WeightTraining: '🏋️',
//     Yoga: '🧘',
//     // Add fallbacks for your backend activity types
//     Running: '🏃',
//     Cycling: '🚴',
//     Swimming: '🏊',
//     Walking: '🚶',
//     Hiking: '🥾',
//     'Weight Training': '🏋️'
//   };

//   return (
//     <div className="space-y-6">
//       <Card className="w-full">
//         <CardHeader>
//           <CardTitle>Workout Recommendations</CardTitle>
//         </CardHeader>
//         <CardContent>
//           <div className="flex flex-col space-y-4">
//             <div className="flex items-center space-x-4">
//               <label className="text-sm font-medium" htmlFor="caloriesInput">
//                 Calories to burn:
//               </label>
//               <input
//                 type="number"
//                 id="caloriesInput"
//                 className="border rounded p-2 w-24"
//                 value={caloriesInput}
//                 onChange={(e) => setCaloriesInput(parseInt(e.target.value) || 0)}
//                 min="1"
//               />
//               <button
//                 className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
//                 onClick={fetchWorkoutSuggestions}
//                 disabled={loading}
//               >
//                 {loading ? 'Loading...' : 'Get Recommendations'}
//               </button>
//             </div>

//             {error && (
//               <div className="text-red-500 mt-2">
//                 Error: {error}
//               </div>
//             )}
//           </div>
//         </CardContent>
//       </Card>

//       {workouts && workouts.length > 0 && (
//         <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
//           {workouts.map((workout, index) => (
//             <Card key={index} className="w-full hover:shadow-lg transition-shadow">
//               <CardHeader className="bg-gray-50">
//                 <CardTitle className="flex items-center text-lg">
//                   <span className="text-2xl mr-2">
//                     {activityIcons[workout.activity] || '💪'}
//                   </span>
//                   {workout.activity}
//                 </CardTitle>
//               </CardHeader>
//               <CardContent className="pt-4">
//                 <ul className="space-y-2">
//                   <li className="flex justify-between">
//                     <span className="text-gray-600">Duration:</span>
//                     <span className="font-medium">{workout.duration_minutes} minutes</span>
//                   </li>
                  
//                   {workout.distance_km !== undefined && (
//                     <li className="flex justify-between">
//                       <span className="text-gray-600">Distance:</span>
//                       <span className="font-medium">{workout.distance_km} km</span>
//                     </li>
//                   )}
                  
//                   {workout.pace && (
//                     <li className="flex justify-between">
//                       <span className="text-gray-600">Pace:</span>
//                       <span className="font-medium">{workout.pace}</span>
//                     </li>
//                   )}
                  
//                   {workout.steps && (
//                     <li className="flex justify-between">
//                       <span className="text-gray-600">Steps:</span>
//                       <span className="font-medium">{workout.steps.toLocaleString()}</span>
//                     </li>
//                   )}
                  
//                   <li className="flex justify-between pt-2 border-t mt-2">
//                     <span className="text-gray-600">Calories:</span>
//                     <span className="font-medium">{workout.estimated_calories} cal</span>
//                   </li>
//                 </ul>
//               </CardContent>
//             </Card>
//           ))}
//         </div>
//       )}
      
//       {workouts && workouts.length === 0 && !loading && (
//         <div className="text-center p-6 bg-gray-50 rounded-lg">
//           No workout recommendations found. Try a different calorie target.
//         </div>
//       )}
//     </div>
//   );
// };

// export default WorkoutRecommendations;