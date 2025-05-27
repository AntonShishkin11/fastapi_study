from typing import Optional, List

from pydantic import BaseModel, Field


class Student(BaseModel):
    last_name: str = Field(default='Не указано')
    first_name: str = Field(default='Не указано')
    faculty: str = Field(default='Не указан')
    course: str = Field(default='Не указан')
    mark: int = Field(default=0)

class StudentUpdate(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    faculty: Optional[str] = None
    course: Optional[str] = None
    mark: Optional[int] = None

class DeleteStudentsRequest(BaseModel):
    ids: List[int]

class ImportCSVRequest(BaseModel):
    path: str
