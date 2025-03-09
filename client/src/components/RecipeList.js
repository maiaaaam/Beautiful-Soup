import React from 'react';
import '../styles/components/RecipeList.css';

const RecipeList = ({ recipes, onRecipeSelect, selectedRecipeId }) => {
    if (!recipes || recipes.length === 0) {
        return (
            <div className="recipe-list empty">
                <p>No recipes found. Try selecting different ingredients.</p>
            </div>
        );
    }
    
    return (
        <div className="recipe-list">
            <h2>Suggested Recipes</h2>
            <div className="recipes-container">
                {recipes.map(recipe => (
                    <div 
                        key={recipe.id} 
                        className={`recipe-card ${selectedRecipeId === recipe.id ? 'selected' : ''}`}
                        onClick={() => onRecipeSelect(recipe)}
                    >
                        <div className="recipe-image">
                            {recipe.image ? (
                                <img src={recipe.image} alt={recipe.title} />
                            ) : (
                                <div className="no-image">No Image</div>
                            )}
                        </div>
                        <div className="recipe-info">
                            <h3>{recipe.title}</h3>
                            <p>Ready in {recipe.readyInMinutes || '?'} minutes</p>
                            {recipe.sourceName && (
                                <p className="source">By {recipe.sourceName}</p>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default RecipeList;