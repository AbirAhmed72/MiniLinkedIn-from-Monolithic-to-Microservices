# post_service/app/api/user_apis.py
import base64
from datetime import timedelta
import io, httpx
from fastapi.responses import JSONResponse
import os
from typing import List
import uuid
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import schemas, database, services, models
from minio import Minio
from datetime import datetime, timedelta, time
from dotenv import load_dotenv

user_service_base_url = "http://user_service:8000"
post_service_base_url = "http://post_service:8001"
notification_service_base_url = "http://notification_service:8002"
# minio_base_url = "http://minio:9000"


post = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "http://127.0.0.1:8000/api/v1/login")
load_dotenv()

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER")
MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD")
MINIO_SECURE = os.getenv("MINIO_SECURE").lower() == "true"

# Initialize MinIO client
minio_client = Minio(
    endpoint=MINIO_ENDPOINT,
    access_key=MINIO_ROOT_USER,
    secret_key=MINIO_ROOT_PASSWORD,
    secure=MINIO_SECURE
)

@post.post('/post')
async def create_post(post_text: str = Form(...), image: UploadFile = File(None), token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    try:
        user_info = await services.get_user_info(token)
        username = user_info["username"]
        print(username)
        image_url = None
        if image:
            # Generate a unique filename for the image
            image_filename = f"{username}_{uuid.uuid4().hex}.jpg"
            # print(image_filename)

            # Save the image to bytes and send to MinIO bucket
            image_bytes = await image.read()

            bucket_name = 'minilinkedindistributed'

            if(minio_client.bucket_exists(bucket_name)):

                minio_client.put_object(
                    "minilinkedindistributed",
                    image_filename,
                    io.BytesIO(image_bytes),  
                    length=len(image_bytes),
                    content_type="image/jpeg"
                )
            
                # Construct the image URL based on MinIO server URL and bucket name
                image_url = f"http://localhost:9000/minilinkedindistributed/{image_filename}"
                print(image_url)

            else:

                try:
                    minio_client.make_bucket("minilinkedindistributed")
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Failed to create bucket: {str(e)}")
            
                try:
                    minio_client.set_bucket_policy("minilinkedindistributed", 
                        policy='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":"*","Action":["s3:GetObject","s3:PutObject"],"Resource":["arn:aws:s3:::minilinkedindistributed/*"]}]}'
                    )
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Failed to set bucket policy: {str(e)}")

                minio_client.put_object(
                    "minilinkedindistributed",
                    image_filename,
                    io.BytesIO(image_bytes),  
                    length=len(image_bytes),
                    content_type="image/jpeg"
                )
            
                # Construct the image URL based on MinIO server URL and bucket name
                image_url = f"http://localhost:9000/minilinkedindistributed/{image_filename}"
                print(image_url)
            
        elif image is None or image.filename == '':
            # raise HTTPException(status_code=400, detail='Invalid or empty image file')
            new_post = services.make_post(db, username, post_text, 'no_image')
        # Create the post
        new_post = services.make_post(db, username, post_text, image_url)

        headers = {"Authorization": f"Bearer {token}"}

        # Get all users (except the one who posted)
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{user_service_base_url}/api/v1/all_users_except_poster", headers=headers)

        if response.status_code == 200:
            all_users_except_poster = response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch users from user service")

        # Create a notification for each user
        for user_to_notify in all_users_except_poster:
            notification_data = {
                'notification_text': f"{username} made a new post...",
                'pid' : new_post.id,
                'username' : user_to_notify["username"],
                'notification_datetime' : datetime.utcnow().isoformat(),
                'is_read' : False
            }

            
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{notification_service_base_url}/api/v1/notification", json=notification_data, headers=headers)

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to send notification")
        

        return{"message" : new_post}
    
    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error for debugging
        return JSONResponse(status_code=500, content={"error": str(e)})


@post.get('/post', response_model=List[schemas.PostData])
async def get_posts(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    user = await services.get_user_info(token)

    if user is None:
        raise services.credentials_exception
    
    # Get all posts except the current user's posts
    latest_posts = services.get_latest_posts(db, user )
    # posts = await db.query(models.Post).filter(models.Post.username != user.username).order_by(models.Post.created_at.desc()).all()


    return latest_posts
