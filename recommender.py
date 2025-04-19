import numpy as np
from sklearn.cluster import KMeans
from sqlalchemy.orm import Session
from models import Movie, User, UserPreference
import pandas as pd

class MovieRecommender:
    def __init__(self, db: Session):
        self.db = db
        self.kmeans = KMeans(n_clusters=5, random_state=42)
        self.movie_features = None
        self.cluster_labels = None
        
    def prepare_features(self):
        # Film özelliklerini hazırla
        movies = self.db.query(Movie).all()
        features = []
        movie_ids = []
        
        for movie in movies:
            # Film özelliklerini vektöre dönüştür
            genre_count = len(movie.genre.split(',')) if movie.genre else 0
            feature = [
                float(movie.rating),
                int(movie.release_year),
                genre_count
            ]
            features.append(feature)
            movie_ids.append(movie.id)
            
        self.movie_features = np.array(features)
        self.movie_ids = np.array(movie_ids)
        
    def fit(self):
        self.prepare_features()
        if len(self.movie_features) > 0:  # En az bir film varsa
            self.cluster_labels = self.kmeans.fit_predict(self.movie_features)
        else:
            self.cluster_labels = np.array([])  # Boş array
        
    def get_user_cluster(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user or not user.watched_movies:
            return None
            
        watched_movie_ids = [movie.id for movie in user.watched_movies]
        watched_clusters = []
        
        for movie_id in watched_movie_ids:
            if movie_id in self.movie_ids and self.cluster_labels is not None:
                idx = np.where(self.movie_ids == movie_id)[0]
                if len(idx) > 0:
                    watched_clusters.append(self.cluster_labels[idx[0]])
                
        if not watched_clusters:
            return None
            
        return max(set(watched_clusters), key=watched_clusters.count)
        
    def recommend_movies(self, user_id: int, n_recommendations: int = 5):
        if self.cluster_labels is None:
            self.fit()
            
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
            
        if not user.watched_movies:
            # Eğer kullanıcı hiç film izlememişse, en yüksek puanlı filmleri öner
            return self.db.query(Movie).order_by(Movie.rating.desc()).limit(n_recommendations).all()
            
        user_cluster = self.get_user_cluster(user_id)
        if user_cluster is None:
            return self.db.query(Movie).order_by(Movie.rating.desc()).limit(n_recommendations).all()
            
        cluster_movies = self.movie_ids[self.cluster_labels == user_cluster]
        
        watched_movie_ids = [movie.id for movie in user.watched_movies]
        recommended_movie_ids = [mid for mid in cluster_movies if mid not in watched_movie_ids]
        
        return self.db.query(Movie).filter(Movie.id.in_(recommended_movie_ids)).order_by(Movie.rating.desc()).limit(n_recommendations).all() 