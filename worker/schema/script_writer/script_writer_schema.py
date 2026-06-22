from pydantic import BaseModel, Field
from typing import List

class Scene(BaseModel):
    title: str = Field(description="The title of the scene, summarizing what is displayed visually.")
    narration: str = Field(description="The narration script this scene.")

class ScriptSchema(BaseModel):
    scenes: List[Scene] = Field(description="A sequential list of scenes that make up the complete video script.")
