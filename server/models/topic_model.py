import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pickle
import os

class RecipeTopicModel:
    def __init__(self, n_topics=10):
        self.n_topics = n_topics
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english'
        )
        self.lda_model = LatentDirichletAllocation(
            n_components=n_topics,
            random_state=42
        )
        self.trained = False
        self.recipe_topics = {}
        
    def preprocess_recipes(self, recipes):
        """
        Prepare recipes for topic modeling
        """
        texts = []
        recipe_ids = []
        
        for recipe in recipes:
            # Combine title, ingredients, and instructions
            recipe_text = f"{recipe.get('title', '')} "
            
            # Add ingredients
            ingredients = recipe.get('extendedIngredients', [])
            ingredient_text = ' '.join([ing.get('name', '') for ing in ingredients])
            recipe_text += ingredient_text
            
            # Add instructions if available
            if 'instructions' in recipe and recipe['instructions']:
                recipe_text += ' ' + recipe['instructions']
                
            texts.append(recipe_text)
            recipe_ids.append(recipe.get('id'))
            
        return texts, recipe_ids
        
    def train(self, recipes):
        """
        Train the topic model on recipes
        """
        texts, recipe_ids = self.preprocess_recipes(recipes)
        
        # Create TF-IDF features
        X = self.vectorizer.fit_transform(texts)
        
        # Train LDA model
        self.lda_model.fit(X)
        
        # Assign topics to recipes
        recipe_topics = self.lda_model.transform(X)
        
        # Store recipe topic assignments
        for i, recipe_id in enumerate(recipe_ids):
            self.recipe_topics[recipe_id] = recipe_topics[i]
            
        self.trained = True
        return self.recipe_topics
    
    def predict_topic(self, recipe):
        """
        Predict the topic distribution for a new recipe
        """
        if not self.trained:
            raise ValueError("Model must be trained before prediction")
            
        texts, _ = self.preprocess_recipes([recipe])
        X = self.vectorizer.transform(texts)
        topic_dist = self.lda_model.transform(X)[0]
        
        return topic_dist
    
    def get_similar_recipes(self, recipe_id, top_n=5):
        """
        Find similar recipes based on topic similarity
        """
        if not self.trained or recipe_id not in self.recipe_topics:
            return []
            
        target_topics = self.recipe_topics[recipe_id]
        
        # Calculate similarity
        similarities = {}
        for rid, topics in self.recipe_topics.items():
            if rid != recipe_id:
                # Cosine similarity
                similarity = np.dot(target_topics, topics) / (
                    np.linalg.norm(target_topics) * np.linalg.norm(topics)
                )
                similarities[rid] = similarity
                
        # Sort by similarity and return top N
        sorted_recipes = sorted(
            similarities.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return [rid for rid, _ in sorted_recipes[:top_n]]
    
    def save_model(self, filepath="models/topic_model.pkl"):
        """
        Save the trained model
        """
        if not self.trained:
            raise ValueError("Cannot save untrained model")
            
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump({
                'vectorizer': self.vectorizer,
                'lda_model': self.lda_model,
                'recipe_topics': self.recipe_topics,
                'n_topics': self.n_topics,
                'trained': self.trained
            }, f)
            
    def load_model(self, filepath="models/topic_model.pkl"):
        """
        Load a trained model
        """
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
            
        self.vectorizer = model_data['vectorizer']
        self.lda_model = model_data['lda_model']
        self.recipe_topics = model_data['recipe_topics']
        self.n_topics = model_data['n_topics']
        self.trained = model_data['trained']