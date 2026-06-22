from pydantic import BaseModel, Field
from typing import List

class StoryboardScene(BaseModel):
    title: str = Field(description="The title of the storyboard scene matching the script.")
    visuals_steps: List[str] = Field(description="A step-by-step list of visual/animation instructions describing what happens on screen.")

class StoryboardSchema(BaseModel):
    scenes: List[StoryboardScene] = Field(description="A list of storyboard scenes mapping directly to the script.")
