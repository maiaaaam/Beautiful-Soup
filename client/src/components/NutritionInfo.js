import React from 'react';
import '../styles/components/NutritionInfo.css';

const NutritionInfo = ({ nutrition }) => {
    if (!nutrition) {
        return (
            <div className="nutrition-info">
                <h2>Nutrition Information</h2>
                <p>No nutrition information available for this recipe.</p>
            </div>
        );
    }
    
    // Extract main macronutrients
    const calories = nutrition.calories || 'N/A';
    const protein = nutrition.protein || 'N/A';
    const carbs = nutrition.carbs || 'N/A';
    const fat = nutrition.fat || 'N/A';
    
    // Additional nutrients if available
    const nutrients = nutrition.nutrients || [];
    
    return (
        <div className="nutrition-info">
            <h2>Nutrition Information</h2>
            
            <div className="macro-summary">
                <div className="macro-item">
                    <div className="macro-value">{calories}</div>
                    <div className="macro-name">Calories</div>
                </div>
                <div className="macro-item">
                    <div className="macro-value">{protein}</div>
                    <div className="macro-name">Protein</div>
                </div>
                <div className="macro-item">
                    <div className="macro-value">{carbs}</div>
                    <div className="macro-name">Carbs</div>
                </div>
                <div className="macro-item">
                    <div className="macro-value">{fat}</div>
                    <div className="macro-name">Fat</div>
                </div>
            </div>
            
            {nutrients.length > 0 && (
                <div className="detailed-nutrients">
                    <h3>Detailed Nutrients</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Nutrient</th>
                                <th>Amount</th>
                                <th>% Daily Value</th>
                            </tr>
                        </thead>
                        <tbody>
                            {nutrients.map((nutrient, index) => (
                                <tr key={index}>
                                    <td>{nutrient.name}</td>
                                    <td>{nutrient.amount} {nutrient.unit}</td>
                                    <td>{nutrient.percentOfDailyNeeds?.toFixed(1)}%</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default NutritionInfo;