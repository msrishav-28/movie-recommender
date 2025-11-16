"""
Movie-related database models.
Includes Movie, Genre, Cast, Crew, and related entities.
"""

from sqlalchemy import Column, String, Integer, Float, Date, Text, ForeignKey, Table, Index, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from app.db.database import Base


# Association tables for many-to-many relationships
movie_genres = Table(
    'movie_genres',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete='CASCADE'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id', ondelete='CASCADE'), primary_key=True),
    Index('idx_movie_genres_movie', 'movie_id'),
    Index('idx_movie_genres_genre', 'genre_id')
)

movie_keywords = Table(
    'movie_keywords',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete='CASCADE'), primary_key=True),
    Column('keyword_id', Integer, ForeignKey('keywords.id', ondelete='CASCADE'), primary_key=True)
)


class Movie(Base):
    """Core movie table with comprehensive metadata."""
    
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    tmdb_id = Column(Integer, unique=True, index=True)
    imdb_id = Column(String(20), unique=True, index=True)
    
    # Basic info
    title = Column(String(500), nullable=False, index=True)
    original_title = Column(String(500))
    tagline = Column(Text)
    overview = Column(Text)
    
    # Release info
    release_date = Column(Date, index=True)
    status = Column(String(50))  # Released, Post Production, etc.
    runtime = Column(Integer)  # minutes
    
    # Production
    budget = Column(Integer)
    revenue = Column(Integer)
    original_language = Column(String(10))
    
    # Ratings and popularity
    vote_average = Column(Float, index=True)
    vote_count = Column(Integer)
    popularity = Column(Float, index=True)
    
    # Media
    poster_path = Column(String(500))
    backdrop_path = Column(String(500))
    trailer_url = Column(String(500))
    
    # Sentiment aggregates (computed from reviews)
    sentiment_score = Column(Float)  # -1 to 1
    sentiment_positive_ratio = Column(Float)  # 0 to 1
    emotion_scores = Column(JSONB)  # {joy: 0.8, sadness: 0.2, ...}
    
    # Computed features for recommendation
    content_embedding_id = Column(String(100))  # Pinecone ID
    average_rating = Column(Float)
    rating_count = Column(Integer, default=0)
    
    # Multi-dimensional averages
    avg_plot_rating = Column(Float)
    avg_acting_rating = Column(Float)
    avg_cinematography_rating = Column(Float)
    avg_soundtrack_rating = Column(Float)
    
    # Aesthetic features
    dominant_colors = Column(JSONB)  # Array of color hex codes
    visual_tags = Column(ARRAY(String))  # rain, sunset, urban, etc.
    cinematography_style = Column(String(100))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_scraped_at = Column(DateTime(timezone=True))
    
    # Relationships
    genres = relationship("Genre", secondary=movie_genres, back_populates="movies")
    keywords = relationship("Keyword", secondary=movie_keywords, back_populates="movies")
    cast = relationship("MovieCast", back_populates="movie", cascade="all, delete-orphan")
    crew = relationship("MovieCrew", back_populates="movie", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="movie", cascade="all, delete-orphan")
    frames = relationship("MovieFrame", back_populates="movie", cascade="all, delete-orphan")
    streaming = relationship("MovieStreaming", back_populates="movie", cascade="all, delete-orphan")
    watchlist_items = relationship("WatchlistItem", back_populates="movie", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_movie_title', 'title'),
        Index('idx_movie_release_date', 'release_date'),
        Index('idx_movie_popularity', 'popularity'),
        Index('idx_movie_vote_average', 'vote_average'),
        Index('idx_movie_rating', 'average_rating'),
    )
    
    def __repr__(self):
        return f"<Movie {self.title} ({self.release_date.year if self.release_date else 'N/A'})>"


class Genre(Base):
    """Movie genres."""
    
    __tablename__ = "genres"
    
    id = Column(Integer, primary_key=True)
    tmdb_id = Column(Integer, unique=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    
    # Relationships
    movies = relationship("Movie", secondary=movie_genres, back_populates="genres")
    
    def __repr__(self):
        return f"<Genre {self.name}>"


class Keyword(Base):
    """Movie keywords for enhanced search and recommendations."""
    
    __tablename__ = "keywords"
    
    id = Column(Integer, primary_key=True)
    tmdb_id = Column(Integer, unique=True)
    name = Column(String(200), unique=True, nullable=False, index=True)
    
    # Relationships
    movies = relationship("Movie", secondary=movie_keywords, back_populates="keywords")
    
    def __repr__(self):
        return f"<Keyword {self.name}>"


class Person(Base):
    """People (actors, directors, crew)."""
    
    __tablename__ = "people"
    
    id = Column(Integer, primary_key=True)
    tmdb_id = Column(Integer, unique=True, index=True)
    imdb_id = Column(String(20), unique=True)
    
    name = Column(String(200), nullable=False, index=True)
    biography = Column(Text)
    birthday = Column(Date)
    deathday = Column(Date)
    place_of_birth = Column(String(200))
    profile_path = Column(String(500))
    popularity = Column(Float)
    
    gender = Column(Integer)  # 0=Unknown, 1=Female, 2=Male, 3=Non-binary
    known_for_department = Column(String(100))  # Acting, Directing, etc.
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    cast_roles = relationship("MovieCast", back_populates="person", cascade="all, delete-orphan")
    crew_roles = relationship("MovieCrew", back_populates="person", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_person_name', 'name'),
        Index('idx_person_popularity', 'popularity'),
    )
    
    def __repr__(self):
        return f"<Person {self.name}>"


class MovieCast(Base):
    """Movie cast members (actors)."""
    
    __tablename__ = "movie_cast"
    
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    person_id = Column(Integer, ForeignKey("people.id", ondelete="CASCADE"), primary_key=True)
    
    character_name = Column(String(500))
    cast_order = Column(Integer)  # 0 is lead role
    
    # Relationships
    movie = relationship("Movie", back_populates="cast")
    person = relationship("Person", back_populates="cast_roles")
    
    __table_args__ = (
        Index('idx_cast_movie', 'movie_id'),
        Index('idx_cast_person', 'person_id'),
        Index('idx_cast_order', 'cast_order'),
    )
    
    def __repr__(self):
        return f"<MovieCast {self.character_name}>"


class MovieCrew(Base):
    """Movie crew members (directors, writers, etc.)."""
    
    __tablename__ = "movie_crew"
    
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    person_id = Column(Integer, ForeignKey("people.id", ondelete="CASCADE"), primary_key=True)
    job = Column(String(100), primary_key=True)  # Director, Writer, Cinematographer, etc.
    
    department = Column(String(100))  # Directing, Writing, Camera, etc.
    
    # Relationships
    movie = relationship("Movie", back_populates="crew")
    person = relationship("Person", back_populates="crew_roles")
    
    __table_args__ = (
        Index('idx_crew_movie', 'movie_id'),
        Index('idx_crew_person', 'person_id'),
        Index('idx_crew_job', 'job'),
    )
    
    def __repr__(self):
        return f"<MovieCrew {self.job}>"


class Collection(Base):
    """Movie collections (franchises, series)."""
    
    __tablename__ = "collections"
    
    id = Column(Integer, primary_key=True)
    tmdb_id = Column(Integer, unique=True)
    
    name = Column(String(500), nullable=False)
    overview = Column(Text)
    poster_path = Column(String(500))
    backdrop_path = Column(String(500))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Collection {self.name}>"


class ProductionCompany(Base):
    """Production companies."""
    
    __tablename__ = "production_companies"
    
    id = Column(Integer, primary_key=True)
    tmdb_id = Column(Integer, unique=True)
    
    name = Column(String(200), nullable=False, index=True)
    logo_path = Column(String(500))
    origin_country = Column(String(2))
    
    def __repr__(self):
        return f"<ProductionCompany {self.name}>"


class Country(Base):
    """Countries for movie production."""
    
    __tablename__ = "countries"
    
    code = Column(String(2), primary_key=True)  # ISO 3166-1
    name = Column(String(100), nullable=False)
    
    def __repr__(self):
        return f"<Country {self.name}>"


class Language(Base):
    """Languages for movies."""
    
    __tablename__ = "languages"
    
    code = Column(String(10), primary_key=True)  # ISO 639-1
    name = Column(String(100), nullable=False)
    english_name = Column(String(100))
    
    def __repr__(self):
        return f"<Language {self.name}>"
