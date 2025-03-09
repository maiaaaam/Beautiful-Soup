import React, { useState, useEffect } from 'react';
import '../styles/components/IngredientSelector.css';

const IngredientSelector = ({ onIngredientsChange }) => {
    const [ingredients, setIngredients] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    
    // Common ingredients for suggestions (would ideally come from an API)
    const commonIngredients = [
        'Chicken', 'Beef', 'Pork', 'Salmon', 'Tuna',
        'Rice', 'Pasta', 'Potato', 'Sweet Potato', 'Quinoa',
        'Tomato', 'Onion', 'Garlic', 'Bell Pepper', 'Carrot',
        'Broccoli', 'Spinach', 'Kale', 'Lettuce', 'Mushroom',
        'Cheese', 'Milk', 'Butter', 'Yogurt', 'Cream',
        'Olive Oil', 'Vegetable Oil', 'Soy Sauce', 'Vinegar', 'Lemon'
    ];
    
    useEffect(() => {
        // When ingredients change, notify parent component
        onIngredientsChange(ingredients);
    }, [ingredients, onIngredientsChange]);
    
    const handleInputChange = (e) => {
        const value = e.target.value;
        setInputValue(value);
        
        if (value.trim() !== '') {
            // Filter suggestions based on input
            const filtered = commonIngredients.filter(ing => 
                ing.toLowerCase().includes(value.toLowerCase())
            );
            setSuggestions(filtered);
        } else {
            setSuggestions([]);
        }
    };
    
    const addIngredient = (ingredient) => {
        const trimmed = ingredient.trim();
        if (trimmed && !ingredients.includes(trimmed)) {
            setIngredients([...ingredients, trimmed]);
            setInputValue('');
            setSuggestions([]);
        }
    };
    
    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && inputValue.trim()) {
            addIngredient(inputValue);
        }
    };
    
    const removeIngredient = (index) => {
        const newIngredients = [...ingredients];
        newIngredients.splice(index, 1);
        setIngredients(newIngredients);
    };
    
    return (
        <div className="ingredient-selector">
            <h2>Select Your Ingredients</h2>
            <div className="input-container">
                <input
                    type="text"
                    value={inputValue}
                    onChange={handleInputChange}
                    onKeyDown={handleKeyDown}
                    placeholder="Type an ingredient and press Enter"
                />
                <button onClick={() => addIngredient(inputValue)}>Add</button>
            </div>
            
            {suggestions.length > 0 && (
                <ul className="suggestions">
                    {suggestions.slice(0, 5).map((suggestion, index) => (
                        <li key={index} onClick={() => addIngredient(suggestion)}>
                            {suggestion}
                        </li>
                    ))}
                </ul>
            )}
            
            <div className="selected-ingredients">
                {ingredients.map((ingredient, index) => (
                    <div key={index} className="ingredient-tag">
                        <span>{ingredient}</span>
                        <button onClick={() => removeIngredient(index)}>×</button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default IngredientSelector;