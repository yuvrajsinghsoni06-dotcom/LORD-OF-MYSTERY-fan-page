import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tarot_db.db")
