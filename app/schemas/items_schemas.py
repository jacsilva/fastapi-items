#!/usr/bin/python

from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime 


class ItemBase(BaseModel):
    title: str
    content: str
    
 
# response_model
class Item(ItemBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True


class CreateItems(ItemBase):
    status: int = None
    group_id: int = None

    class Config:
        orm_mode = True


class UpdateItems(ItemBase):
    status: int = None
    group_id: int = None

    class Config:
        orm_mode = True

