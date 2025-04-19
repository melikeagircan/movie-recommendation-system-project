from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models
from config import engine, get_db
from recommender import MovieRecommender
from pydantic import BaseModel
from passlib.context import CryptContext

# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Recommendation System")

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic modelleri
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class MovieCreate(BaseModel):
    title: str
    genre: str
    release_year: int
    description: str
    rating: float

class MovieResponse(BaseModel):
    id: int
    title: str
    genre: str
    release_year: int
    description: str
    rating: float

    class Config:
        orm_mode = True

# Kullanıcı işlemleri
@app.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Film işlemleri
@app.post("/movies/", response_model=MovieResponse)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.get("/movies/", response_model=List[MovieResponse])
def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movies = db.query(models.Movie).offset(skip).limit(limit).all()
    return movies

# Film izleme ve puanlama
@app.post("/users/{user_id}/watch/{movie_id}")
def watch_movie(user_id: int, movie_id: int, rating: float, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    
    if not user or not movie:
        raise HTTPException(status_code=404, detail="User or movie not found")
    
    # Kullanıcı-film ilişkisini güncelle
    user.watched_movies.append(movie)
    db.commit()
    return {"message": "Movie watched successfully"}

# Öneri sistemi
@app.get("/users/{user_id}/recommendations", response_model=List[MovieResponse])
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    recommender = MovieRecommender(db)
    try:
        recommended_movies = recommender.recommend_movies(user_id)
        return recommended_movies
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 