# post_service/app/main.py

from fastapi import FastAPI
from app.api.post_apis import post
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(openapi_url="/api/v1/post/openapi.json", docs_url="/api/v1/post/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post, prefix="/api/v1", tags=['Post'])
