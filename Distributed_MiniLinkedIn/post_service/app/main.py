# post_service/app/main.py

from fastapi import FastAPI
from app.api.post_apis import post
from fastapi.middleware.cors import CORSMiddleware
from app.api.create_tables import create_tables

# user_service_base_url = "http://user_service:8000"
# post_service_base_url = "http://post_service:8001"
# notification_service_base_url = "http://notification_service:8002"


app = FastAPI(openapi_url="/api/v1/post/openapi.json", docs_url="/api/v1/post/docs")

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

app.include_router(post, prefix="/api/v1", tags=['Post'])
