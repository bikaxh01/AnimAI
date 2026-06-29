from pydantic import BaseModel
import uuid

class MessagePayload(BaseModel):
    id: str
    status: str
    prompt: str
