# post_service/app/api/services.py

from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import Integer
from . import models, schemas
from datetime import datetime, time, timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session
import httpx

user_service_base_url = "http://user_service:8000"
post_service_base_url = "http://post_service:8001"
notification_service_base_url = "http://notification_service:8002"

credentials_exception = HTTPException(
        status_code=401,
        detail="Could not Validate the credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

async def get_user_info(token: str):
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
    posts = db.query(models.Post).order_by(models.Post.created_at.desc()).all()

    latest_posts = []
    for post in posts:
        post_data = schemas.PostData(
            post_text=post.post_text,
            image_url=post.image_url,
            post_datetime=post.created_at.timestamp(),
            username=post.username
        )
        latest_posts.append(post_data)
    
    return latest_posts
