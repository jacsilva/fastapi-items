#!/usr/bin/python

from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime 


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
