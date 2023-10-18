# post_service/app/api/schemas.py

from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel

class PostCreate(BaseModel):
    post_text: str
    image_url: Optional[UploadFile]
    
    class Config:
        from_attributes = True

class PostData(BaseModel):
    post_text: str
    image_url: Optional[str] = None
    post_datetime: float
    # post_datetime: datetime
    username: str
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
