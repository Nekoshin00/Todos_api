from pydantic import BaseModel

class Status(BaseModel):
    id: int
    name: str

class CreateStatus(BaseModel):
    name: str