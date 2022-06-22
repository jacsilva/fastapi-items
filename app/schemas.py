#!/usr/bin/python

from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app import config
from fastapi import Depends

class CreateItems(BaseModel):
    # id: int
    title: str
    content: str
    # status = str
    # group_id = int

    class Config:
        orm_mode = True

 