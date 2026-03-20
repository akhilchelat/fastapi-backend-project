from pydantic import BaseModel, EmailStr
from typing import Optional

class CreateUser(BaseModel):
    name: str
    email: str
    password: str
    role: str

class UpdateUser(BaseModel):
    user_id: int 
    name: Optional[str] = None
    email: Optional[str] = None 
    role: Optional[str] = None 

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str 


