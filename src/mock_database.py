import random
import pandas as pd
from datetime import datetime, timedelta

# 1. DEFINING PERSONAS (To make it relatable)
# Instead of "User 42", we have "Uncle Bob" who loves Action.
PERSONAS = {
    0: {"name": "Action Andy", "avatar": "👮", "bio": "Loves explosions and car chases.", "fav_genre": "Action"},
    1: {"name": "RomCom Rachel", "avatar": "🍷", "bio": "Looking for love in New York City.", "fav_genre": "Romance"},
    2: {"name": "SciFi Sam", "avatar": "👽", "bio": "I want to believe.", "fav_genre": "Sci-Fi"},
    3: {"name": "Drama Dave", "avatar": "🎭", "bio": "Here for the tears.", "fav_genre": "Drama"},
    42: {"name": "The New Guy", "avatar": "👶", "bio": "Just joined yesterday. No history.", "fav_genre": "Unknown"}
}

MOVES_TITLES_PARTS = {
    "Action": ["Thunder", "Force", "Strike", "Explosion", "Agent", "Revenge", "Protocol"],
    "Sci-Fi": ["Star", "Galaxy", "Quantum", "Cyber", "Moon", "Dimension", "Mars"],
    "Romance": ["Love", "Heart", "Kiss", "Summer", "Wedding", "Paris", "Date"],
    "Comedy": ["Laugh", "Party", "Mistake", "Boss", "Vacation", "Dad", "Cat"]
}

class MockDatabase:
    def __init__(self, num_users, num_movies):
        self.num_users = num_users
        self.num_movies = num_movies
        self.movie_metadata = self._generate_movie_metadata()
        
    def _generate_movie_metadata(self):
        """Generates fake titles and genres for all movies"""
        metadata = {}
        for i in range(self.num_movies):
            genre = random.choice(list(MOVES_TITLES_PARTS.keys()))
            title = f"{random.choice(MOVES_TITLES_PARTS[genre])} {random.choice(MOVES_TITLES_PARTS[genre])}"
            if random.random() > 0.8: title += f" {random.randint(2, 5)}" # Sequel
            
            metadata[i] = {
                "title": title,
                "genre": genre,
                "year": random.randint(1980, 2024),
                "poster_color": self._get_color(genre)
            }
        return metadata

    def _get_color(self, genre):
        colors = {"Action": "#e74c3c", "Sci-Fi": "#8e44ad", "Romance": "#e91e63", "Comedy": "#f1c40f"}
        return colors.get(genre, "#95a5a6")

    def get_user_profile(self, user_id):
        """Returns a rich profile for the user"""
        if user_id in PERSONAS:
            return PERSONAS[user_id]
        
        # Procedural generation for other users
        return {
            "name": f"User {user_id}", 
            "avatar": "👤", 
            "bio": "A mysterious movie watcher.",
            "fav_genre": "Mixed"
        }

    def get_user_history(self, user_id):
        """Simulates a 'Recently Watched' list"""
        # If Cold Start, return empty
        if user_id == 42: return []
        
        history = []
        for _ in range(random.randint(3, 8)):
            mid = random.randint(0, self.num_movies-1)
            history.append(self.movie_metadata[mid])
        return history

    def enrich_recommendations(self, df):
        """Merges the raw GNN output with our fake metadata"""
        enriched = []
        for _, row in df.iterrows():
            mid = int(row['movie_id'])
            meta = self.movie_metadata.get(mid, {"title": f"Movie {mid}", "genre": "Unknown", "year": 2020})
            
            item = row.to_dict()
            item.update(meta)
            enriched.append(item)
        return pd.DataFrame(enriched)
    

# """
# CODE EXPLANATION:
# 1. Purpose: To simulate a real production database (like SQL) for the demo.
# 2. PERSONAS: A dictionary of hardcoded 'demo users' (Action Andy, etc.) to show distinct behaviors.
# 3. _generate_movie_metadata():
#    - Since the MovieLens dataset only provides IDs (e.g., Movie 500), this function invents titles.
#    - It uses random combinations of words (Thunder + Strike) to create fake movie names.
#    - It assigns random Genres and Colors for the UI cards.
# 4. enrich_recommendations():
#    - Takes the raw math output from the GNN (Movie ID: 500, Rating: 4.5).
#    - Joins it with the fake metadata (Title: "Thunder Strike", Genre: "Action").
#    - This turns raw numbers into a product users can understand.
# """