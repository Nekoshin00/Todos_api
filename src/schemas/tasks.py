from pydantic import BaseModel
from typing import List

class Task(BaseModel):
    id: int
    folder_id: int
    status_id: int
    title: str
    description: str | None = None

class TaskCreate(BaseModel):
    title: str
    description: str | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

class TaskStatusUpdate(BaseModel):
    status_id: int

class TasksResponse(BaseModel):
    tasks: List[Task]
    total_pages: int
    total_count: int