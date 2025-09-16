from typing import Optional
from pydantic import BaseModel, EmailStr

class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    session_id: str
