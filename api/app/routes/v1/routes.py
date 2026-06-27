from fastapi import APIRouter
from app.routes.v1.endpoints import project

api_router = APIRouter()
api_router.include_router(project.router, prefix="/projects", tags=["Projects"])
