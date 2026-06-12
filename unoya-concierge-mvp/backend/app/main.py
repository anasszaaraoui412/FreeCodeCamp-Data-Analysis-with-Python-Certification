from fastapi import FastAPI
from app.core.config import settings
from app.api.deps import get_current_user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to UNOYA AI Workplace Concierge API"}

from app.api.api_v1.api import api_router

app.include_router(api_router, prefix=settings.API_V1_STR)
