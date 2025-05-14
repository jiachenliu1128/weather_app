from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load database URL or default to current directory SQLite database
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", default="sqlite:///./weather.db")

# Create engine, session maker and base class 
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()

# Create a new database session for each request
def get_db():
    """
    Create a new database session for each request.
    
    Returns:
        A database session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
        
        