from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base # Replace with your actual module and model names

SQL_DATABASE_URL = "postgresql://postgres:1234@localhost:5432/Notification"

# Replace 'your_database_url' with your actual PostgreSQL database URL
engine = create_engine(SQL_DATABASE_URL)

# Create a session factory
Session = sessionmaker(bind=engine)

# Create the tables based on your models
Base.metadata.create_all(bind=engine)