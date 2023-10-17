# post_service/app/api/models.py

from sqlalchemy import Column, DateTime, Integer, String, Boolean
from app.api.database import Base

class Notification(Base):
    __tablename__ = 'notifications'
    nid = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    pid = Column(Integer, nullable=False)
    notification_text = Column(String(50), nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime)
