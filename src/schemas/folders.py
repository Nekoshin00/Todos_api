from pydantic import BaseModel


class Folder(BaseModel):
    id: int
    user_id: int
    name: str
    description: str | None = None

class CreateFolder(BaseModel):
    name: str
    description: str | None = None

class UpdateFolder(BaseModel):
    name: str | None = None
    description: str | None = None