import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from app.db import get_session
from app.models.project import Project, ProjectStatus

router = APIRouter()

class ProjectCreate(BaseModel):
    prompt: str

class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    code_file: str | None = None
    video_url: str | None = None
    status: ProjectStatus | None = None

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

@router.patch("/{pid}", response_model=Project)
def update_project(pid: uuid.UUID, project_in: ProjectUpdate, session: Session = Depends(get_session)):
    project = session.get(Project, pid)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = project_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)
        
    project.updated_at = datetime.now(timezone.utc)
    
    session.add(project)
    session.commit()
    session.refresh(project)
    return project
