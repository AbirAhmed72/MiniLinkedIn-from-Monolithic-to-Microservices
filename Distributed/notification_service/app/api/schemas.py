# post_service/app/api/schemas.py

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class NotificationCreate(BaseModel):
    notification_text: str
    is_read: bool = False
    # notification_datetime: float
    notification_datetime: datetime
    pid: int
    username: str
    class Config:
        from_attributes = True

class NotificationData(BaseModel):
    notification_datetime: datetime
    notification_text: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    class Config:
        from_attributes = True
class TokenData(BaseModel):
    username: Optional[str] = None
    class Config:
        from_attributes = True

# Define other schemas as needed
