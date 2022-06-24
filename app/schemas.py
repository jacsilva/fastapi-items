#!/usr/bin/python

from pydantic import BaseModel
from datetime import datetime 


class Item(BaseModel):
    id: int
    title: str
    content: str
    status = str
    group_id = int
    created_at: datetime
    
    class Config:
        orm_mode = True

        
class ItemBase(BaseModel):
    title: str
    content: str
    status = str
    group_id = int

    class Config:
        orm_mode = True


class CreateItems(ItemBase):
    pass


class UpdateItems(ItemBase):
    pass


class GroupBase(BaseModel):
    title: str 

    class Config:
        orm_mode = True


class CreateGroups(GroupBase):
    pass

