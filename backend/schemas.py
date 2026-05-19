from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class AlertBase(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=100)
    location: str = Field(..., min_length=1, max_length=100)

class AlertCreate(AlertBase):
    pass

class Alert(AlertBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Job(BaseModel):
    id: int
    linkedin_id: str
    title: str
    company: str
    location: str
    link: str
    alert_id: int
    discovered_at: datetime
    emailed: bool

    class Config:
        from_attributes = True
