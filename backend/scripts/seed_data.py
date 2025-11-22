"""
Database Seeding Script
Populates database with sample data for development and testing.
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime, date

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.security import get_password_hash
from app.db.models.user import User, UserPreferences
from app.db.models.movie import Movie, Genre
from app.db.models.rating import Rating, Review
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def seed_genres(session: AsyncSession):
    """Seed movie genres."""
    logger.info("Seeding genres...")
    
    genres = [
        Genre(id=28, name="Action"),
        Genre(id=12, name="Adventure"),
        Genre(id=16, name="Animation"),
        Genre(id=35, name="Comedy"),
        Genre(id=80, name="Crime"),
        Genre(id=99, name="Documentary"),
        Genre(id=18, name="Drama"),
        Genre(id=10751, name="Family"),
        Genre(id=14, name="Fantasy"),
        Genre(id=36, name="History"),
        Genre(id=27, name="Horror"),
        Genre(id=10402, name="Music"),
        Genre(id=9648, name="Mystery"),
        Genre(id=10749, name="Romance"),
        Genre(id=878, name="Science Fiction"),
        Genre(id=10770, name="TV Movie"),
        Genre(id=53, name="Thriller"),
        Genre(id=10752, name="War"),
        Genre(id=37, name="Western"),
    ]
    
    for genre in genres:
        session.add(genre)
    
    await session.commit()
    logger.info(f"✅ Created {len(genres)} genres")


async def seed_users(session: AsyncSession):
    """Seed test users."""
    logger.info("Seeding users...")
    
    users = [
        User(
            email="admin@cineaesthete.com",
            username="admin",
            password_hash=get_password_hash("Admin@123"),
            full_name="Admin User",
            is_admin=True,
            is_verified=True,
            is_premium=True
        ),
        User(
            email="john.doe@example.com",
            username="johndoe",
            password_hash=get_password_hash("Password@123"),
            full_name="John Doe",
            is_verified=True,
            bio="Movie enthusiast and critic"
        ),
        User(
            email="jane.smith@example.com",
            username="janesmith",
            password_hash=get_password_hash("Password@123"),
            full_name="Jane Smith",
            is_verified=True,
            is_premium=True,
            bio="Film director and cinephile"
        ),
    ]
    
    for user in users:
        session.add(user)
        
        # Add preferences
        prefs = UserPreferences(
            user_id=user.id,
            favorite_genres=["Drama", "Science Fiction", "Thriller"],
            preferred_moods=["intense", "thought-provoking"],
            diversity_preference=7,
            enable_llm_recommendations=True,
            enable_aesthetic_search=True,
            enable_gnn_recommendations=True
        )
        session.add(prefs)
    
    await session.commit()
    logger.info(f"✅ Created {len(users)} users with preferences")
    
    return users


async def seed_movies(session: AsyncSession):
    """Seed sample movies."""
    logger.info("Seeding movies...")
    
    movies = [
        Movie(
            id=550,
            title="Fight Club",
            original_title="Fight Club",
            overview="A ticking-time-bomb insomniac and a slippery soap salesman channel primal male aggression into a shocking new form of therapy.",
            release_date=date(1999, 10, 15),
            runtime=139,
            vote_average=8.4,
            vote_count=26000,
            popularity=50.0,
            original_language="en",
            poster_path="/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
            backdrop_path="/hZkgoQYus5vegHoetLkCJzb17zJ.jpg"
        ),
        Movie(
            id=13,
            title="Forrest Gump",
            original_title="Forrest Gump",
            overview="A man with a low IQ has accomplished great things and been present during significant historic events.",
            release_date=date(1994, 6, 23),
            runtime=142,
            vote_average=8.5,
            vote_count=24000,
            popularity=45.0,
            original_language="en",
            poster_path="/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
            backdrop_path="/7c9UVPPiTPltouxRVY6N9uUakom.jpg"
        ),
        Movie(
            id=27205,
            title="Inception",
            original_title="Inception",
            overview="A thief who steals corporate secrets through the use of dream-sharing technology is given the task of planting an idea.",
            release_date=date(2010, 7, 15),
            runtime=148,
            vote_average=8.4,
            vote_count=32000,
            popularity=55.0,
            original_language="en",
            poster_path="/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
            backdrop_path="/s3TBrRGB1iav7gFOCNx3H31MoES.jpg"
        ),
        Movie(
            id=680,
            title="Pulp Fiction",
            original_title="Pulp Fiction",
            overview="A burger-loving hit man, his philosophical partner, and a washed-up boxer collide in this crime caper.",
            release_date=date(1994, 9, 10),
            runtime=154,
            vote_average=8.5,
            vote_count=25000,
            popularity=48.0,
            original_language="en",
            poster_path="/fIE3lAGcZDV1G6XM5KmuWnNsPp1.jpg",
            backdrop_path="/4cDFJr4HnXN5AdPw4AKrmLlMWdO.jpg"
        ),
        Movie(
            id=155,
            title="The Dark Knight",
            original_title="The Dark Knight",
            overview="Batman must accept one of the greatest psychological and physical tests to fight injustice.",
            release_date=date(2008, 7, 14),
            runtime=152,
            vote_average=8.5,
            vote_count=30000,
            popularity=60.0,
            original_language="en",
            poster_path="/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
            backdrop_path="/hkBaDkMWbLaf8B1lsWsKX7Ew3Xq.jpg"
        ),
    ]
    
    for movie in movies:
        session.add(movie)
    
    await session.commit()
    logger.info(f"✅ Created {len(movies)} movies")
    
    return movies


async def seed_ratings_and_reviews(session: AsyncSession, users, movies):
    """Seed sample ratings and reviews."""
    logger.info("Seeding ratings and reviews...")
    
    count = 0
    
    # John rates Fight Club
    rating1 = Rating(
        user_id=users[1].id,
        movie_id=movies[0].id,
        overall_rating=5.0,
        plot_rating=5.0,
        acting_rating=5.0,
        cinematography_rating=4.5
    )
    session.add(rating1)
    
    review1 = Review(
        user_id=users[1].id,
        movie_id=movies[0].id,
        rating_id=rating1.id,
        title="Mind-blowing masterpiece!",
        content="Fight Club is an absolute masterpiece. The cinematography is stunning, the acting is phenomenal, and the plot twist at the end is unforgettable. A must-watch for any film enthusiast.",
        sentiment_score=0.95,
        sentiment_label="positive",
        sentiment_confidence=0.98
    )
    session.add(review1)
    count += 1
    
    # Jane rates Inception
    rating2 = Rating(
        user_id=users[2].id,
        movie_id=movies[2].id,
        overall_rating=4.8,
        plot_rating=5.0,
        acting_rating=4.5,
        cinematography_rating=5.0,
        soundtrack_rating=5.0
    )
    session.add(rating2)
    
    review2 = Review(
        user_id=users[2].id,
        movie_id=movies[2].id,
        rating_id=rating2.id,
        title="Visually stunning and intellectually challenging",
        content="Nolan delivers another masterpiece with Inception. The visual effects are groundbreaking, Hans Zimmer's score is perfection, and the narrative complexity keeps you engaged throughout. A truly immersive experience.",
        sentiment_score=0.92,
        sentiment_label="positive",
        sentiment_confidence=0.96,
        likes_count=15
    )
    session.add(review2)
    count += 1
    
    # John rates The Dark Knight
    rating3 = Rating(
        user_id=users[1].id,
        movie_id=movies[4].id,
        overall_rating=5.0,
        plot_rating=5.0,
        acting_rating=5.0,
        cinematography_rating=5.0,
        soundtrack_rating=5.0
    )
    session.add(rating3)
    count += 1
    
    await session.commit()
    logger.info(f"✅ Created {count} ratings and reviews")


async def main():
    """Main seeding function."""
    print("\n" + "="*60)
    print("CineAesthete Database Seeding")
    print("="*60 + "\n")
    
    # Create async engine
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    
    # Create session factory
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    try:
        async with async_session() as session:
            # Seed data
            await seed_genres(session)
            users = await seed_users(session)
            movies = await seed_movies(session)
            await seed_ratings_and_reviews(session, users, movies)
        
        print("\n" + "="*60)
        print("✅ Database seeding complete!")
        print("="*60 + "\n")
        
        print("Sample user credentials:")
        print("  Admin: admin@cineaesthete.com / Admin@123")
        print("  User1: john.doe@example.com / Password@123")
        print("  User2: jane.smith@example.com / Password@123")
        print()
        
        print("You can now start the application!")
        print()
        
    except Exception as e:
        logger.error(f"❌ Seeding failed: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
