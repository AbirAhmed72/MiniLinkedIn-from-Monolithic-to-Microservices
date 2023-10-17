# models.py
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, PrimaryKeyConstraint
from database import Base

from sqlalchemy import  Column, Integer, String, Boolean, DateTime, Text

class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)  # Add unique constraint
    password_hashed = Column(String)
    posts = relationship('Post', back_populates='users')
    notifications = relationship('Notification', back_populates='users')


class Post(Base):
    __tablename__ = 'posts'
    pid = Column(Integer, primary_key=True, index=True)
    post_text = Column(String, nullable=False)
    image_url = Column(String(255))
    created_at = Column(DateTime)
    username = Column(String(100), ForeignKey('users.username'), nullable=False)  # Ensure the correct reference
    users = relationship('User', back_populates='posts')
    notifications = relationship('Notification', back_populates='posts')


class Notification(Base):
    __tablename__ = 'notifications'
    nid = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), ForeignKey('users.username'), nullable=False)
    pid = Column(Integer, ForeignKey('posts.pid'), nullable=False)
    notification_text = Column(String(50), nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime)

    # Relationship with User table
    users = relationship('User', back_populates='notifications')
    # Relationship with Post table
    posts = relationship('Post', back_populates='notifications')