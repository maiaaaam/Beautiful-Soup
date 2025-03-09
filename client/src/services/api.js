// Base URL for our backend API
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Helper function for API requests
const fetchWithTimeout = async (url, options = {}, timeout = 10000) => {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);
    
    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal
        });
        
        clearTimeout(id);
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        if (error.name === 'AbortError') {
            throw new Error('Request timeout');
        }
        throw error;
    }
};

// API functions
export const getRecipesByIngredients = async (ingredients) => {
    const ingredientsParam = ingredients.join(',');
    return fetchWithTimeout(
        `${API_BASE_URL}/recipes?ingredients=${encodeURIComponent(ingredientsParam)}`
    );
};

export const getRecipeDetails = async (recipeId) => {
    return fetchWithTimeout(`${API_BASE_URL}/recipes/${recipeId}`);
};

export const getRecipeNutrition = async (recipeId) => {
    return fetchWithTimeout(`${API_BASE_URL}/recipes/${recipeId}/nutrition`);
};

export const getSimilarRecipes = async (recipeId) => {
    return fetchWithTimeout(`${API_BASE_URL}/recipes/similar?recipe_id=${recipeId}`);
};

export const getFlavorSuggestions = async (ingredients) => {
    const ingredientsParam = ingredients.join(',');
    return fetchWithTimeout(
        `${API_BASE_URL}/flavor/suggestions?ingredients=${encodeURIComponent(ingredientsParam)}`
    );
};

export const searchTastyRecipes = async (ingredients) => {
    const ingredientsParam = ingredients.join(',');
    return fetchWithTimeout(
        `${API_BASE_URL}/tasty/search?ingredients=${encodeURIComponent(ingredientsParam)}`
    );
};

export const getTastyRecipeDetails = async (url) => {
    return fetchWithTimeout(
        `${API_BASE_URL}/tasty/recipe?url=${encodeURIComponent(url)}`
    );
};

export const getWorkoutSuggestions = async (calories) => {
    return fetchWithTimeout(`${API_BASE_URL}/workout?calories=${calories}`);
};

export const generateRecipeWithSLM = async (ingredients, flavorNotes = []) => {
    return fetchWithTimeout(
        `${API_BASE_URL}/slm/generate-recipe`, 
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ ingredients, flavor_notes: flavorNotes })
        }
    );
};

export const trainModels = async (recipes) => {
    return fetchWithTimeout(
        `${API_BASE_URL}/models/train`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ recipes })
        }
    );
};