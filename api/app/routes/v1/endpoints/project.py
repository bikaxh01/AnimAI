import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from app.db import get_session
from app.models.project import Project, ProjectStatus

router = APIRouter()

class ProjectCreate(BaseModel):
    prompt: str

@router.post("/", response_model=Project)
def create_project(project_in: ProjectCreate, session: Session = Depends(get_session)):
    project = Project(prompt=project_in.prompt)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

@router.get("/", response_model=list[Project])
def get_projects(session: Session = Depends(get_session)):
    statement = (
        select(Project)
        .where(Project.status != ProjectStatus.FAILED)
        .order_by(Project.created_at.desc())
    )
    projects = session.exec(statement).all()
    return projects

@router.get("/{pid}", response_model=Project)
def get_project(pid: uuid.UUID, session: Session = Depends(get_session)):
    project = session.get(Project, pid)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
