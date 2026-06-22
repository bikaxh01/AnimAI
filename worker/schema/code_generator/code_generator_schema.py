from pydantic import BaseModel, Field

class CodeGenerationSchema(BaseModel):
    code: str = Field(description="The complete, runnable Manim Python code.")
    summary: str = Field(description="A brief summary of what the code implements.")
