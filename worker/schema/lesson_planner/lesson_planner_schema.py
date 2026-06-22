from pydantic import BaseModel, Field
from typing import List

class LessonPlannerSchema(BaseModel):
    title: str = Field(
        description="the title should be small to too big human readbale"
    )
    description: str = Field(
        description="This should be short not too long around 80-100 words"
    )
    concepts: List[str] = Field(
        description="this field will include all the concepts that need ot be covered to full fill the user prompt"
    )
