import React, { useState } from 'react';
import '../styles/components/WorkoutSuggestion.css';

const WorkoutSuggestion = ({ workouts, calories }) => {
    const [selectedExercise, setSelectedExercise] = useState(null);
    
    if (!workouts || workouts.length === 0) {
        return (
            <div className="workout-suggestion">
                <h2>Workout Suggestions</h2>
                <p>No workout suggestions available for this recipe.</p>
            </div>
        );
    }
    
    // Calculate how many minutes to burn calories
    const calculateDuration = (exercise) => {
        if (!exercise || !exercise.calories_burned || exercise.calories_burned === 0) {
            return 'N/A';
        }
        
        const caloriesPerMinute = exercise.calories_burned / exercise.duration;
        const minutesToBurn = Math.ceil(calories / caloriesPerMinute);
        
        return minutesToBurn;
    };
    
    return (
        <div className="workout-suggestion">
            <h2>Burn Those Calories</h2>
            <p className="calorie-info">
                This recipe contains approximately <strong>{calories} calories</strong> per serving.
            </p>
            
            <div className="workout-options">
                <h3>Choose an activity to burn it off:</h3>
                <div className="exercise-cards">
                    {workouts.map((exercise, index) => (
                        <div 
                            key={index} 
                            className={`exercise-card ${selectedExercise === index ? 'selected' : ''}`}
                            onClick={() => setSelectedExercise(index)}
                        >
                            <h4>{exercise.name}</h4>
                            <div className="exercise-details">
                                <p>
                                    <strong>{exercise.calories_burned}</strong> calories per {exercise.duration} minutes
                                </p>
                                <p className="duration-estimate">
                                    Burn this meal in: <strong>{calculateDuration(exercise)} minutes</strong>
                                </p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
            
            {selectedExercise !== null && (
                <div className="workout-detail">
                    <h3>Your Workout Plan</h3>
                    <div className="workout-plan">
                        <p>
                            <strong>{workouts[selectedExercise].name}</strong> for {calculateDuration(workouts[selectedExercise])} minutes
                        </p>
                        <p className="workout-tips">
                            Tips: Stay hydrated and maintain proper form throughout your workout.
                            Listen to your body and adjust intensity as needed.
                        </p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default WorkoutSuggestion;