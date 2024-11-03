from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class Command(BaseModel):
    command_name: Optional[str] = None
    participants: List[str] = Field(default_factory=list)

class Account(BaseModel):
    login: str
    password: str
    command_list: List[Command] = Field(default_factory=list)
    favorites: List[str] = Field(default_factory=list)
