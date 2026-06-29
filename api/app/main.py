import uuid
import sys
from loguru import logger
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from pydantic import BaseModel
from app.config.settings import settings
from app.db import create_db_and_tables, get_session
from app.routes.v1.routes import api_router
from app.services.redis_service import redis_service

logger.add("logs/api_{time}.log", rotation="500 MB", level="INFO", enqueue=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    redis_service.connect()
    yield
    redis_service.close()

app = FastAPI(title="API Server", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root(session: Session = Depends(get_session)):
    return {"message": "Welcome to the API Server"}
