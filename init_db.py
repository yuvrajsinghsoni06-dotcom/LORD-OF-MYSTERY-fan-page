import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.database import engine, Base
from app.seed import seed_database

if __name__ == "__main__":
    print("Initializing Database Schema and Seeding Data...")
    Base.metadata.create_all(bind=engine)
    seed_database(force=True)
    print("Database Initialization Complete!")
