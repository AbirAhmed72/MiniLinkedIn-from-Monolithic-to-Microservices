# user_service/app/api/models.py

from sqlalchemy import Column, Integer, String
from app.api.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    password_hashed = Column(String)
    # Other user fields
