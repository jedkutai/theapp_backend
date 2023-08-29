from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class AccountCreateIn(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str

    @validator('username')
    def force_lowercase_username(cls, value):
        return value.lower()
    
    @validator('email')
    def force_lowercase_email(cls, value):
        return value.lower()

    class Config:
        from_attributes = True

class AccountCreateOut(BaseModel):
    name: str
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class AccountViewOut(BaseModel):
    name: str
    username: str
    email: EmailStr
    bio: Optional[str]
    profile_pic: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None