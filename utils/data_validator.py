from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class RoleCreateOneData(BaseModel):
    createdAt: str
    updatedAt: str
    deletedAt: None
    id: int
    name: str
    skills: List[str] # This will always be an empty string
    


class RoleCreateOne(BaseModel):
    data: RoleCreateOneData