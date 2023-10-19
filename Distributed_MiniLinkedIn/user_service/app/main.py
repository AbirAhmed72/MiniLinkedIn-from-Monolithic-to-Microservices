# user_service/app/main.py

from fastapi import FastAPI
from app.api.user_apis import user
from fastapi.middleware.cors import CORSMiddleware
from app.api.create_tables import create_tables
app = FastAPI(openapi_url="/api/v1/user/openapi.json", docs_url="/api/v1/user/docs")

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

app.include_router(user, prefix="/api/v1", tags=['User'])
