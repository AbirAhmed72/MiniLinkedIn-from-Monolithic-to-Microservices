# user_service/app/api/services.py
from datetime import datetime, time, timedelta

from typing import Optional
from passlib.hash import bcrypt
from fastapi import HTTPException
from jose import JWTError
import jwt
from app.api import schemas, models
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


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

def all_users_except_poster(db: Session, username: str):
    return db.query(models.User).filter(models.User.username != username).all()
     