# post_service/app/main.py

from fastapi import FastAPI
from app.api.notification_apis import notification
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from .api import services, database
from app.api.create_tables import create_tables

# user_service_base_url = "http://user_service:8000"
# post_service_base_url = "http://post_service:8001"
# notification_service_base_url = "http://notification_service:8002"

app = FastAPI(openapi_url="/api/v1/notification/openapi.json", docs_url="/api/v1/notification/docs")

@app.on_event("startup")
def startup_event():
    # Initialize database tables
    create_tables()
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notification, prefix="/api/v1", tags=['Notification'])

#background task
scheduler = BackgroundScheduler(daemon=True)
# db_url = os.environ.get("postgresql://postgres:1234@localhost:5432/MiniLinkedIn")  # Replace with your database URL
scheduler.add_job(services.delete_old_notifications, 'interval', args=[next(database.get_db())], minutes=1)

# Start the scheduler
# scheduler.start()
