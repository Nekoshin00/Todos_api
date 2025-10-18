from pydantic import BaseModel

class RefreshTokenRequest(BaseModel):
    refresh_token: str
    
class Register(BaseModel):
    username: str
    email: str
    password: str
    full_name: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None
    username: str | None = None