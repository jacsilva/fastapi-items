#!/usr/bin/python

from typing import List
from pydantic import BaseModel
from datetime import datetime 

        
class ItemBase(BaseModel):
    title: str
    content: str
    status = int
    group_id = int


# response_model
class Item(ItemBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True


class CreateItems(ItemBase):
    pass


class UpdateItems(ItemBase):
    pass




class GroupBase(BaseModel):
    title: str 


class Group(GroupBase):
    title: str 
    items: List[Item] = []
    
    class Config:
        orm_mode = True


class CreateGroups(GroupBase):
    pass







class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
