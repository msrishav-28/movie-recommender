"""
Database Initialization Script
Creates all tables and sets up initial data.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.db.database import Base
from app.db.models import user, movie, rating, watchlist
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_database():
    """Initialize database with all tables."""
    logger.info("Starting database initialization...")
    
    # Create async engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
        future=True
    )
    
    try:
        # Create all tables
        async with engine.begin() as conn:
            logger.info("Dropping existing tables...")
            await conn.run_sync(Base.metadata.drop_all)
            
            logger.info("Creating all tables...")
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("✅ Database initialization complete!")
        logger.info(f"Tables created:")
        for table in Base.metadata.sorted_tables:
            logger.info(f"  - {table.name}")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise
    finally:
        await engine.dispose()


async def verify_database():
    """Verify database connection and tables."""
    logger.info("Verifying database...")
    
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    
    try:
        async with engine.begin() as conn:
            # Try a simple query
            result = await conn.execute("SELECT 1")
            assert result.scalar() == 1
        
        logger.info("✅ Database verification successful!")
        
    except Exception as e:
        logger.error(f"❌ Database verification failed: {e}")
        raise
    finally:
        await engine.dispose()


def main():
    """Main entry point."""
    print("\n" + "="*60)
    print("CineAesthete Database Initialization")
    print("="*60 + "\n")
    
    try:
        # Run initialization
        asyncio.run(init_database())
        
        # Verify
        asyncio.run(verify_database())
        
        print("\n" + "="*60)
        print("✅ Database is ready!")
        print("="*60 + "\n")
        
        print("Next steps:")
        print("1. Run 'python scripts/seed_data.py' to add sample data")
        print("2. Start the application with 'uvicorn app.main:app --reload'")
        print()
        
    except Exception as e:
        print(f"\n❌ Initialization failed: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
