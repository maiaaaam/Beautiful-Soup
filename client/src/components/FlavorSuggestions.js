import React from 'react';
import '../styles/components/FlavorSuggestions.css';

const FlavorSuggestions = ({ suggestions, onAddIngredient }) => {
    if (!suggestions || suggestions.length === 0) {
        return null;
    }
    
    return (
        <div className="flavor-suggestions">
            <h3>Flavor Pairings</h3>
            <p className="suggestion-intro">
                These ingredients would complement your selection:
            </p>
            
            <div className="suggestion-list">
                {suggestions.map((suggestion, index) => (
                    <div key={index} className="suggestion-item">
                        <div className="suggestion-name">{suggestion.name}</div>
                        <div className="suggestion-meta">
                            <div className="affinity" style={{ width: `${suggestion.average_affinity * 100}%` }}>
                                <span className="affinity-label">
                                    {(suggestion.average_affinity * 100).toFixed(0)}% match
                                </span>
                            </div>
                        </div>
                        <button 
                            className="add-button"
                            onClick={() => onAddIngredient(suggestion.name)}
                        >
                            Add
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default FlavorSuggestions;