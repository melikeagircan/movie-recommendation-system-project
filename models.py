from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from config import Base

# Kullanıcı-film ilişki tablosu
user_movie_association = Table(
    'user_movie_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('rating', Float)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    # İlişkiler
    watched_movies = relationship("Movie", secondary=user_movie_association, back_populates="watched_by")
    preferences = relationship("UserPreference", back_populates="user")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genre = Column(String)
    release_year = Column(Integer)
    description = Column(String)
    rating = Column(Float)
    
    # İlişkiler
    watched_by = relationship("User", secondary=user_movie_association, back_populates="watched_movies")

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    genre_preference = Column(String)
    rating_preference = Column(Float)
    
    # İlişkiler
    user = relationship("User", back_populates="preferences") 