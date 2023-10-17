# main.py
import os
import minio, uuid, io
import joblib as jb
import models, schemas, services, database
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Optional

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.sqltypes import Integer
from schemas import TokenData
from sqlalchemy.orm import Session
from database import SessionLocal, engine

from datetime import datetime, timedelta, time
from jose import JWTError,jwt
from minio import Minio
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


minio_client = Minio(
    "127.0.0.1:9000",
    access_key="Abir",
    secret_key="12345678",
    secure=False  # Set to True if using HTTPS
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

    

@app.get("/")
async def root():
    return {"message": "Awesome Mini LinkedIn"}
    

@app.post('/register')
async def register_user(user_data: schemas.UserCreate,  db: Session = Depends(database.get_db)):
    db_user =  services.get_user_by_username(db, user_data.username)
    if db_user:
         raise HTTPException(status_code=400, detail="E-mail already Registered")
    access_token_expires = timedelta(minutes=services.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = services.create_access_token(
        data={"sub": user_data.username}, expires_delta=access_token_expires
    )
    user = services.create_user(db, user_data)
    user.token = access_token
    # return data
    return {"access_token": access_token, "token_type": "bearer"}
    # return data
    # return{"message" : f"User {user.username} registered successfully!"}


@app.post('/token')
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    db_user = services.get_user_by_username(db, form_data.username)
    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not services.verify_hashed_password(form_data.password, db_user.password_hashed):
        raise HTTPException(
            status_code=401,
            detail="Invalid Password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=services.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = services.create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
    # return {"username": user_dict.name}

@app.get('/me')
async def get_current_user_info(token: str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):

    token_data = services.verify_user(token)

    user = services.get_user_by_username(db, token_data.username)
    delattr(user, "password_hashed")

    return user
    
    # return {
    #     "my_info": services.get_user_by_username(db, token_data.username),
    #     "role":"user"
    # }


@app.post('/post')
async def create_post(post_text: str, image: UploadFile = File(None), token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    token_data = services.verify_user(token)

    user = services.get_user_by_username(db, username=token_data.username)
    print(user.username)
    if user is None:
        raise services.credentials_exception

    image_url = None
    if image:
        # Generate a unique filename for the image
        image_filename = f"{user.username}_{uuid.uuid4().hex}.jpg"
        print(image_filename)

        # Save the image to bytes and send to MinIO bucket
        image_bytes = await image.read()

        minio_client.put_object(
            "minilinkedin",
            image_filename,
            io.BytesIO(image_bytes),  
            length=len(image_bytes),
            content_type="image/jpeg"
        )

        # Construct the image URL based on MinIO server URL and bucket name
        image_url = f"http://127.0.0.1:9000/minilinkedin/{image_filename}"
        print(image_url)

    # services.make_post(db, token_data.username, post_text, image_url)

    # Create the post
    new_post = services.make_post(db, token_data.username, post_text, image_url)

    # Get all users (except the one who posted)
    all_users_except_poster = db.query(models.User).filter(models.User.username != user.username).all()

    # Create a notification for each user
    for user_to_notify in all_users_except_poster:
        notification_data = schemas.NotificationCreate(
            notification_text=f"{user.username} made a new post...",
            pid=new_post.pid,
            username=user_to_notify.username,
            notification_datetime=datetime.utcnow()
        )

        services.make_notification(db, notification_data)

    return{"message" : "Post uploaded successfully!"}


@app.get('/post', response_model=List[schemas.PostData])
async def get_posts(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    token_data = services.verify_user(token)

    user = services.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise services.credentials_exception
    
    # Get all posts except the current user's posts
    latest_posts = services.get_latest_posts(db, user)

    return latest_posts


@app.get('/notification')
async def get_notifications(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    token_data = services.verify_user(token)

    user = services.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise services.credentials_exception
    
    unread_notifications = []    
    notifications = services.get_unread_notifications(db, token_data.username)

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


#background task
scheduler = BackgroundScheduler(daemon=True)
db_url = os.environ.get("postgresql://postgres:1234@localhost:5432/MiniLinkedIn")  # Replace with your database URL
scheduler.add_job(services.delete_old_notifications, 'interval', args=[next(database.get_db())], minutes=10)

# Start the scheduler
# scheduler.start()

