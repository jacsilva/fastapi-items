#!/usr/bin/python

from typing import List, Dict
from pydantic import BaseModel, EmailStr
from datetime import datetime 


class UserBase(BaseModel):
    username: str
    email: EmailStr

 
class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True
