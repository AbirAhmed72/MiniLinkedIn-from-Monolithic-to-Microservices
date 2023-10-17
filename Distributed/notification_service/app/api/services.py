# notification_service/app/api/services.py

from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import Integer
from . import models, schemas
from datetime import datetime, time, timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session
import httpx


credentials_exception = HTTPException(
        status_code=401,
        detail="Could not Validate the credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

async def get_user_info(token: str):
    user_service_base_url = "http://127.0.0.1:8000"  # Replace with the actual URL of your user service
    headers = {"Authorization": f"Bearer {token}"}
    print("Request Headers:", headers) 
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{user_service_base_url}/api/v1/me", headers=headers)
        if response.status_code == 200:
            user_info = response.json()
            return user_info
        else:
            # Handle authentication error
            raise HTTPException(status_code=response.status_code, detail="Authentication error")


def make_notification(db: Session, notification_data: schemas.NotificationCreate):
    # Create a Notification object with the provided data
    notification = models.Notification(
        username=notification_data["username"],
        pid=notification_data["pid"],
        notification_text=notification_data["notification_text"],
        is_read=notification_data["is_read"],
        created_at=notification_data["notification_datetime"]
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

