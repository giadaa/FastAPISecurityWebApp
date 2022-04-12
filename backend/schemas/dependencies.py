from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# shared properties
class DependencyBase(BaseModel):
    name: Optional[str] = None
    latest_version: Optional[str] = None
    deadline: Optional[date] = None
    date_posted: Optional[date] = datetime.now().date()


# this will be used to validate data while creating a Dependency
class DependencyCreate(DependencyBase):
    name: str
    latest_version: str
    deadline: date


# this will be used to format the response to not to have id,owner_id etc
class ShowDependency(DependencyBase):
    name: str
    latest_version: str
    deadline: date
    date_posted: date

    class Config:
        orm_mode = True
