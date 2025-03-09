import React from 'react';
import '../styles/components/Reviews.css';

const Reviews = ({ reviews }) => {
    if (!reviews || reviews.length === 0) {
        return (
            <div className="reviews">
                <h2>User Reviews</h2>
                <p>No reviews available for this recipe.</p>
            </div>
        );
    }
    
    // If sentiment analysis is available
    const sentimentAnalysis = reviews.sentiment_analysis || null;
    
    return (
        <div className="reviews">
            <h2>User Reviews</h2>
            
            {sentimentAnalysis && (
                <div className="sentiment-summary">
                    <h3>Review Sentiment</h3>
                    <div className="sentiment-bars">
                        <div className="sentiment-bar">
                            <div className="label">Positive</div>
                            <div className="bar-container">
                                <div 
                                    className="bar positive" 
                                    style={{ width: `${sentimentAnalysis.positive_percentage}%` }}
                                ></div>
                                <span className="percentage">{sentimentAnalysis.positive_percentage.toFixed(1)}%</span>
                            </div>
                        </div>
                        <div className="sentiment-bar">
                            <div className="label">Neutral</div>
                            <div className="bar-container">
                                <div 
                                    className="bar neutral" 
                                    style={{ width: `${sentimentAnalysis.neutral_percentage}%` }}
                                ></div>
                                <span className="percentage">{sentimentAnalysis.neutral_percentage.toFixed(1)}%</span>
                            </div>
                        </div>
                        <div className="sentiment-bar">
                            <div className="label">Negative</div>
                            <div className="bar-container">
                                <div 
                                    className="bar negative" 
                                    style={{ width: `${sentimentAnalysis.negative_percentage}%` }}
                                ></div>
                                <span className="percentage">{sentimentAnalysis.negative_percentage.toFixed(1)}%</span>
                            </div>
                        </div>
                    </div>
                    <p className="sentiment-conclusion">
                        Overall sentiment: <strong>{sentimentAnalysis.overall_sentiment}</strong>
                    </p>
                </div>
            )}
            
            <div className="review-list">
                <h3>User Comments ({Array.isArray(reviews) ? reviews.length : 0})</h3>
                {Array.isArray(reviews) ? (
                    reviews.map((review, index) => (
                        <div 
                            key={index} 
                            className={`review-item ${review.sentiment ? review.sentiment : ''}`}
                        >
                            <div className="review-header">
                                <span className="author">{review.author || 'Anonymous'}</span>
                                {review.date && <span className="date">{review.date}</span>}
                                {review.sentiment && (
                                    <span className={`sentiment-tag ${review.sentiment}`}>
                                        {review.sentiment}
                                    </span>
                                )}
                            </div>
                            <div className="review-content">{review.text}</div>
                        </div>
                    ))
                ) : (
                    <p>Review data format is invalid.</p>
                )}
            </div>
        </div>
    );
};

export default Reviews;