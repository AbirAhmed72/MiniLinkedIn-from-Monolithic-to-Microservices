# services.py
import asyncio
import threading
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import Integer
import models, schemas
from jose import JWTError, jwt #JSON Web Token
from datetime import datetime, time, timedelta
import random
from passlib.hash import bcrypt

from sqlalchemy import create_engine, engine
from sqlalchemy.engine import base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

SECRET_KEY = 'e2c6a3bc1aad22372e102e8f9f657bccd65676aef94587815b9d4d2c4960a650'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

credentials_exception = HTTPException(
        status_code=401,
        detail="Could not Validate the credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

def verify_user(token: str) -> schemas.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username = username)
        return token_data
    except JWTError:
        raise credentials_exception
    
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_hashed_password(password: str):
    return bcrypt.hash(password)

def verify_hashed_password(password: str, password_hashed: str):
    return bcrypt.verify(password, password_hashed)

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = create_hashed_password(user.password)
    db_user = models.User(
        # username = user.username,
        username = user.username,
        password_hashed = hashed_password,
        # is_active = True
    )
    print(db_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    delattr(db_user, "password_hashed")
    return db_user

def get_user_by_username(db: Session, username: str):
    print("Checking existing users")
    return db.query(models.User).filter(models.User.username == username).first()

def get_all_users(db: Session):
    return db.query(models.User).all()

def get_user_by_uid(db: Session, id: int):
    print("Checking existing users")
    return db.query(models.User).filter(models.User.id == id).first()

def get_notification_by_nid(db: Session, nid: int):
    return db.query(models.Notification).filter(models.Notification.nid == nid).first()

def get_post_by_pid(db: Session, pid: int):
    return db.query(models.Post).filter(models.Post.pid == pid).first()

def make_post(db: Session, current_username: str, post_text, image_url: Optional[str] = None):
    db_post = models.Post(
        post_text = post_text,
        image_url = image_url,
        created_at = datetime.utcnow(),
        username = current_username
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_latest_posts(db: Session, user):
    posts = db.query(models.Post).filter(models.Post.username != user.username).order_by(models.Post.created_at.desc()).all()

    latest_posts = []
    for post in posts:
        post_data = schemas.PostData(
            username=post.username,
            post_text=post.post_text,
            image_url=post.image_url,
            post_datetime=post.created_at.timestamp(),
        )
        latest_posts.append(post_data)
    
    return latest_posts

def make_notification(db: Session, notification_data: schemas.NotificationCreate):
    # Create a Notification object with the provided data
    notification = models.Notification(
        username=notification_data.username,
        pid=notification_data.pid,
        notification_text=notification_data.notification_text,
        is_read=notification_data.is_read,
        created_at=notification_data.notification_datetime
    )

    # Add the notification to the database session
    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification

def get_unread_notifications(db: Session, username: str) -> List[models.Notification]:
    return db.query(models.Notification).filter(models.Notification.username == username, models.Notification.is_read == False).all()

def get_old_notifications(db: Session, timestamp: datetime):
    """
    Retrieve notifications older than the given timestamp from the database.

    Args:
        db (Session): SQLAlchemy database session.
        timestamp (datetime): The timestamp to filter notifications.

    Returns:
        List[models.Notification]: List of notifications older than the given timestamp.
    """
    # print(timestamp)

    return db.query(models.Notification).filter(models.Notification.created_at < timestamp).all()


def delete_old_notifications(db: Session):
    # Calculate the timestamp for 1 minute ago
    one_minute_ago = datetime.utcnow() - timedelta(minutes=1)
    print(one_minute_ago)

    # Get notifications older than 1 minute
    old_notifications = get_old_notifications(db, one_minute_ago)

    # Delete the old notifications
    for notification in old_notifications:
        db.delete(notification)

    db.commit()
