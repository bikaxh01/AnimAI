import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlmodel import Session
from app.config.settings import settings
from app.db import create_db_and_tables, get_session
from app.models.user import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="API Server", lifespan=lifespan)

@app.get("/")
def read_root(session: Session = Depends(get_session)):
    # Create a dummy user
    dummy_email = f"dummy_{uuid.uuid4().hex[:8]}@example.com"
    user = User(email=dummy_email)
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return {"message": "Welcome to the API Server", "created_user": user}
