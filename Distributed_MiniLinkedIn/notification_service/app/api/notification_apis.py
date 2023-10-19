# notification_service/app/api/user_apis.py
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.api import schemas, database, services



notification = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "http://127.0.0.1:8000/api/v1/login")

@notification.get('/notification')
async def get_notifications(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    user_info = await services.get_user_info(token)
    username = user_info["username"]
    unread_notifications = []    
    notifications = services.get_unread_notifications(db, username)

    for notification in notifications:
        notification.is_read = True
        db.add(notification)

    db.commit()
    
    for notification in notifications:
        notification_data = schemas.NotificationData(
            notification_text=notification.notification_text,
            notification_datetime=notification.created_at
        )
        unread_notifications.append(notification_data)

    if unread_notifications:
        return unread_notifications
    else: 
        return {"message" : "No pending notifications!"}
    
@notification.post('/notification')
async def create_notifications(notification_data: dict, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    return services.make_notification(db, notification_data)
