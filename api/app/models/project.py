import uuid
from datetime import datetime, timezone
from enum import Enum
from sqlmodel import Field, SQLModel



class ProjectStatus(str, Enum):
    PENDING = "pending"
    PLANNING = "planning"
    WRITING_SCRIPT = "writing_script"
    STORYBOARDING = "storyboarding"
    GENERATING_CODE = "generating_code"
    ANALYZING_CODE = "analyzing_code"
    DEBUGGING = "debugging"
    COMPILING = "compiling"
    COMPLETED = "completed"
    FAILED = "failed"

class Project(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    title: str | None = None
    description: str | None = None
    code_file: str | None = None
    video_url: str | None = None
    prompt: str
    status: ProjectStatus = Field(default=ProjectStatus.PENDING)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
