from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from schema.lesson_planner.lesson_planner_schema import LessonPlannerSchema
from schema.script_writer.script_writer_schema import ScriptSchema
from schema.storyboard.storyboard_schema import StoryboardSchema

class VideoStatus(str, Enum):
    PENDING = "pending"
    PLANNING = "planning"
    WRITING_SCRIPT = "writing_script"
    STORYBOARDING = "storyboarding"
    GENERATING_CODE = "generating_code"
    COMPILING = "compiling"
    COMPLETED = "completed"
    FAILED = "failed"

class AgentState(BaseModel):
    prompt: str
    lesson_plan: Optional[LessonPlannerSchema] = None
    script: Optional[ScriptSchema] = None
    storyboard: Optional[StoryboardSchema] = None
    manim_code: str = ""
    compile_error: List[str] = Field(default_factory=list)
    debug_attempts: int = 0
    has_error : bool = Field(default=False)
    video_path: str = ""
    final_video_path: str = ""
    status: str = VideoStatus.PENDING.value
