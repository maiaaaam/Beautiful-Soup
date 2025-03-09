import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import IngredientSelector from './components/IngredientSelector';
import RecipeList from './components/RecipeList';
import RecipeDetail from './components/RecipeDetail';
import FlavorSuggestions from './components/FlavorSuggestions';
import * as api from './services/api';
import './styles/main.css';

const App = () => {
    const [ingredients, setIngredients] = useState([]);
    const [recipes, setRecipes] = useState([]);
    const [selectedRecipe, setSelectedRecipe] = useState(null);
    const [recipeNutrition, setRecipeNutrition] = useState(null);
    const [recipeReviews, setRecipeReviews] = useState([]);
    const [workouts, setWorkouts] = useState([]);
    const [flavorSuggestions, setFlavorSuggestions] = useState([]);
    const [tastyRecipes, setTastyRecipes] = useState([]);
    const [loading, setLoading] = useState({
        recipes: false,
        tasty: false,
        suggestions: false
    });
    const [error, setError] = useState({
        recipes: null,
        tasty: null,
        suggestions: null
    });

    // Handle ingredient selection
    const handleIngredientsChange = (newIngredients) => {
        setIngredients(newIngredients);
        
        // Clear previous selections when ingredients change
        setSelectedRecipe(null);
        setRecipeNutrition(null);
        setRecipeReviews([]);
        setWorkouts([]);
    };

    // Fetch recipes when ingredients change
    useEffect(() => {
        const fetchData = async () => {
            if (ingredients.length === 0) {
                setRecipes([]);
                setTastyRecipes([]);
                setFlavorSuggestions([]);
                return;
            }
            
            // Fetch recipes from Spoonacular
            setLoading(prev => ({ ...prev, recipes: true }));
            try {
                const recipeData = await api.getRecipesByIngredients(ingredients);
                setRecipes(recipeData);
                setError(prev => ({ ...prev, recipes: null }));
            } catch (err) {
                console.error('Error fetching recipes:', err);
                setError(prev => ({ ...prev, recipes: err.message }));
                setRecipes([]);
            } finally {
                setLoading(prev => ({ ...prev, recipes: false }));
            }
            
            // Fetch recipes from Tasty
            setLoading(prev => ({ ...prev, tasty: true }));
            try {
                const tastyData = await api.searchTastyRecipes(ingredients);
                setTastyRecipes(tastyData);
                setError(prev => ({ ...prev, tasty: null }));
            } catch (err) {
                console.error('Error fetching Tasty recipes:', err);
                setError(prev => ({ ...prev, tasty: err.message }));
                setTastyRecipes([]);
            } finally {
                setLoading(prev => ({ ...prev, tasty: false }));
            }
        }
    })    
}    // TO CONTINUE