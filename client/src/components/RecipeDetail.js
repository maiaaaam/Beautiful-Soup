import React, { useState } from 'react';
import NutritionInfo from './NutritionInfo';
import Reviews from './Reviews';
import WorkoutSuggestion from './WorkoutSuggestion';
import '../styles/components/RecipeDetail.css';

const RecipeDetail = ({ recipe, nutrition, reviews, workouts }) => {
    const [activeTab, setActiveTab] = useState('ingredients');
    
    if (!recipe) {
        return null;
    }
    
    return (
        <div className="recipe-detail">
            <div className="recipe-header">
                <h1>{recipe.title}</h1>
                {recipe.image && (
                    <div className="recipe-main-image">
                        <img src={recipe.image} alt={recipe.title} />
                    </div>
                )}
                <div className="recipe-meta">
                    <div className="meta-item">
                        <span className="label">Ready in:</span>
                        <span className="value">{recipe.readyInMinutes || '?'} minutes</span>
                    </div>
                    <div className="meta-item">
                        <span className="label">Servings:</span>
                        <span className="value">{recipe.servings || '?'}</span>
                    </div>
                    {recipe.sourceName && (
                        <div className="meta-item">
                            <span className="label">Source:</span>
                            <span className="value">{recipe.sourceName}</span>
                        </div>
                    )}
                </div>
            </div>
            
            <div className="recipe-tabs">
                <div 
                    className={`tab ${activeTab === 'ingredients' ? 'active' : ''}`}
                    onClick={() => setActiveTab('ingredients')}
                >
                    Ingredients
                </div>
                <div 
                    className={`tab ${activeTab === 'instructions' ? 'active' : ''}`}
                    onClick={() => setActiveTab('instructions')}
                >
                    Instructions
                </div>
                <div 
                    className={`tab ${activeTab === 'nutrition' ? 'active' : ''}`}
                    onClick={() => setActiveTab('nutrition')}
                >
                    Nutrition
                </div>
                <div 
                    className={`tab ${activeTab === 'reviews' ? 'active' : ''}`}
                    onClick={() => setActiveTab('reviews')}
                >
                    Reviews
                </div>
                <div 
                    className={`tab ${activeTab === 'workout' ? 'active' : ''}`}
                    onClick={() => setActiveTab('workout')}
                >
                    Workout Plan
                </div>
            </div>
            
            <div className="tab-content">
                {activeTab === 'ingredients' && (
                    <div className="ingredients">
                        <h2>Ingredients</h2>
                        <ul>
                            {recipe.extendedIngredients?.map((ingredient, index) => (
                                <li key={index}>
                                    {ingredient.original || `${ingredient.amount} ${ingredient.unit} ${ingredient.name}`}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
                
                {activeTab === 'instructions' && (
                    <div className="instructions">
                        <h2>Instructions</h2>
                        {recipe.analyzedInstructions?.length > 0 ? (
                            <ol>
                                {recipe.analyzedInstructions[0].steps.map(step => (
                                    <li key={step.number}>
                                        {step.step}
                                    </li>
                                ))}
                            </ol>
                        ) : recipe.instructions ? (
                            <div dangerouslySetInnerHTML={{ __html: recipe.instructions }} />
                        ) : (
                            <p>No instructions available.</p>
                        )}
                    </div>
                )}
                
                {activeTab === 'nutrition' && (
                    <NutritionInfo nutrition={nutrition} />
                )}
                
                {activeTab === 'reviews' && (
                    <Reviews reviews={reviews} />
                )}
                
                {activeTab === 'workout' && (
                    <WorkoutSuggestion 
                        workouts={workouts} 
                        calories={nutrition?.calories || 0}
                    />
                )}
            </div>
        </div>
    );
};

export default RecipeDetail;