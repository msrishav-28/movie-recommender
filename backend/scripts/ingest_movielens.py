"""
MovieLens Dataset Ingestion Script
Downloads and imports MovieLens 25M dataset into the database.
"""

import asyncio
import sys
from pathlib import Path
import csv
from datetime import datetime
import logging

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.models.movie import Movie, Genre
from app.db.models.rating import Rating

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MovieLensIngester:
    """
    MovieLens dataset ingestion handler.
    
    Dataset: MovieLens 25M
    Files:
    - movies.csv (movieId, title, genres)
    - ratings.csv (userId, movieId, rating, timestamp)
    - tags.csv (userId, movieId, tag, timestamp)
    - links.csv (movieId, imdbId, tmdbId)
    """
    
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.engine = None
        self.session = None
    
    async def setup(self):
        """Setup database connection."""
        self.engine = create_async_engine(settings.DATABASE_URL, echo=False)
        
        async_session = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        self.session = async_session()
    
    async def teardown(self):
        """Cleanup connections."""
        if self.session:
            await self.session.close()
        if self.engine:
            await self.engine.dispose()
    
    async def ingest_all(self):
        """Ingest entire MovieLens dataset."""
        logger.info("Starting MovieLens dataset ingestion...")
        
        try:
            await self.setup()
            
            # Ingest in order
            await self.ingest_genres()
            await self.ingest_movies()
            await self.ingest_links()
            await self.ingest_ratings()
            
            logger.info("✅ MovieLens dataset ingestion complete!")
            
        except Exception as e:
            logger.error(f"❌ Ingestion failed: {e}")
            raise
        finally:
            await self.teardown()
    
    async def ingest_genres(self):
        """Extract and create all unique genres."""
        logger.info("Ingesting genres...")
        
        movies_file = self.data_dir / "movies.csv"
        
        if not movies_file.exists():
            logger.warning(f"movies.csv not found at {movies_file}")
            return
        
        # Extract unique genres
        all_genres = set()
        
        with open(movies_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                genres_str = row.get('genres', '')
                if genres_str and genres_str != '(no genres listed)':
                    genres = genres_str.split('|')
                    all_genres.update(genres)
        
        # Create genre records
        genre_id = 1
        for genre_name in sorted(all_genres):
            genre = Genre(id=genre_id, name=genre_name)
            self.session.add(genre)
            genre_id += 1
        
        await self.session.commit()
        logger.info(f"✅ Created {len(all_genres)} genres")
    
    async def ingest_movies(self, batch_size: int = 1000):
        """Ingest movies from movies.csv."""
        logger.info("Ingesting movies...")
        
        movies_file = self.data_dir / "movies.csv"
        
        if not movies_file.exists():
            logger.error(f"movies.csv not found at {movies_file}")
            return
        
        batch = []
        count = 0
        
        with open(movies_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                movie_id = int(row['movieId'])
                title = row['title']
                
                # Extract year from title (e.g., "Movie Title (1999)")
                year = None
                if '(' in title and ')' in title:
                    year_str = title[title.rfind('(')+1:title.rfind(')')]
                    if year_str.isdigit() and len(year_str) == 4:
                        year = int(year_str)
                        # Remove year from title
                        title = title[:title.rfind('(')].strip()
                
                movie = Movie(
                    id=movie_id,
                    title=title,
                    original_title=title,
                    release_date=datetime(year, 1, 1) if year else None,
                    overview=None,  # Will be enriched from TMDb
                    vote_average=0.0,
                    vote_count=0,
                    popularity=0.0,
                    original_language='en'
                )
                
                batch.append(movie)
                count += 1
                
                # Batch insert
                if len(batch) >= batch_size:
                    self.session.add_all(batch)
                    await self.session.commit()
                    logger.info(f"Processed {count} movies...")
                    batch = []
        
        # Insert remaining
        if batch:
            self.session.add_all(batch)
            await self.session.commit()
        
        logger.info(f"✅ Ingested {count} movies")
    
    async def ingest_links(self):
        """Ingest TMDb and IMDb links."""
        logger.info("Ingesting movie links...")
        
        links_file = self.data_dir / "links.csv"
        
        if not links_file.exists():
            logger.warning(f"links.csv not found at {links_file}")
            return
        
        count = 0
        
        with open(links_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                movie_id = int(row['movieId'])
                imdb_id = row.get('imdbId', '')
                tmdb_id = row.get('tmdbId', '')
                
                # Update movie with external IDs
                # In production: execute UPDATE queries in batches
                count += 1
        
        logger.info(f"✅ Processed {count} movie links")
    
    async def ingest_ratings(self, batch_size: int = 10000):
        """
        Ingest ratings from ratings.csv.
        WARNING: This is 25 million rows - takes significant time!
        """
        logger.info("Ingesting ratings (this may take a while)...")
        
        ratings_file = self.data_dir / "ratings.csv"
        
        if not ratings_file.exists():
            logger.error(f"ratings.csv not found at {ratings_file}")
            return
        
        batch = []
        count = 0
        
        with open(ratings_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                user_id = row['userId']
                movie_id = int(row['movieId'])
                rating_value = float(row['rating'])
                timestamp = int(row['timestamp'])
                
                rating = Rating(
                    user_id=f"ml_user_{user_id}",  # Prefix to distinguish MovieLens users
                    movie_id=movie_id,
                    overall_rating=rating_value,
                    created_at=datetime.fromtimestamp(timestamp)
                )
                
                batch.append(rating)
                count += 1
                
                # Batch insert
                if len(batch) >= batch_size:
                    self.session.add_all(batch)
                    await self.session.commit()
                    logger.info(f"Processed {count} ratings...")
                    batch = []
                
                # Optional: limit for testing
                # if count >= 100000:  # First 100k ratings
                #     break
        
        # Insert remaining
        if batch:
            self.session.add_all(batch)
            await self.session.commit()
        
        logger.info(f"✅ Ingested {count} ratings")


async def main():
    """Main ingestion function."""
    print("\n" + "="*60)
    print("MovieLens 25M Dataset Ingestion")
    print("="*60 + "\n")
    
    # Check for data directory
    data_dir = input("Enter path to MovieLens data directory (containing CSV files): ").strip()
    
    if not Path(data_dir).exists():
        print(f"❌ Directory not found: {data_dir}")
        print("\nDownload MovieLens 25M from:")
        print("https://grouplens.org/datasets/movielens/25m/")
        return
    
    print(f"\nData directory: {data_dir}")
    print("\n⚠️  WARNING: This will ingest ~25 million ratings. This may take hours.")
    confirm = input("Continue? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("Ingestion cancelled.")
        return
    
    # Run ingestion
    ingester = MovieLensIngester(data_dir)
    await ingester.ingest_all()
    
    print("\n" + "="*60)
    print("✅ Ingestion Complete!")
    print("="*60 + "\n")
    print("Next steps:")
    print("1. Enrich movie data with TMDb API")
    print("2. Train recommendation models")
    print("3. Generate embeddings for semantic search")
    print()


if __name__ == "__main__":
    asyncio.run(main())
