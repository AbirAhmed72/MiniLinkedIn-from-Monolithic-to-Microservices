# post_service/app/api/models.py

from sqlalchemy import Column, DateTime, Integer, String
from app.api.database import Base

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    post_text = Column(String, nullable=False)
    image_url = Column(String(255))
    created_at = Column(DateTime)
    username = Column(String(100), nullable=False)  # Ensure the correct reference

