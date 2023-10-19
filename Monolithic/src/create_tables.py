import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base # Replace with your actual module and model names
from dotenv import load_dotenv

load_dotenv()

# Get the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Replace 'your_database_url' with your actual PostgreSQL database URL
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_table():
# Create the tables based on your models
    Base.metadata.create_all(bind=engine)