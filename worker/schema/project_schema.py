import uuid
from enum import Enum
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class ProjectStatus(str, Enum):
    PENDING = "pending"
    PLANNING = "planning"
    WRITING_SCRIPT = "writing_script"
    STORYBOARDING = "storyboarding"
    GENERATING_CODE = "generating_code"
    COMPILING = "compiling"
    COMPLETED = "completed"
    FAILED = "failed"

class Project(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    
    title: str | None = None
    description: str | None = None
    code_file: str | None = None
    video_url: str | None = None
    prompt: str
    status: ProjectStatus = Field(default=ProjectStatus.PENDING)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
