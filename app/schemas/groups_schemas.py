#!/usr/bin/python

from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime 
from .docs_schemas import Item

class GroupBase(BaseModel):
    title: str 


class Group(GroupBase):
    id: int 
    items: List[Item] = []
    
    class Config:
        orm_mode = True


class CreateGroups(GroupBase):
    pass


