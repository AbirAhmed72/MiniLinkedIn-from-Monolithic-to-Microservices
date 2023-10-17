# user_service/app/api/schemas.py

from typing import Optional
from pydantic import BaseModel

class UserData(BaseModel):
    uid: int
    username: str
    class Config:
        from_attributes = True
class UserCreate(BaseModel):
    username: str
    password: str
    class Config:
        from_attributes = True

class ResponseUserData(UserData):
    token: str
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
