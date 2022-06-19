#!/usr/bin/python

from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app import config
from fastapi import Depends

class CreateItems(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None



class CreateDocs(BaseModel):
    title: str
    content: str
    status: int

# async def conn_string(settings = Depends(config.get_settings)):
#     return {'string': settings.database_string }

def conn_string (settings = Depends(config.get_settings)):
   
    try:
        conn = psycopg2.connect (dbname='sinfordby',
                           user = 'DtS28Hbfac',
                           password = "qlS8mYmDUnsKXJflZDM7FouCLDWYpEiV",
                           host = "10.0.52.89",
                           port='5432'
                           )
        cursor = conn.cursor()
        print("Database connected!\n")

        return cursor
        # cur.execute("UPDATE image SET ip='" + ip + "' WHERE id=" + iid)
        # db.commit()
    except BaseException as error:
        ret = False
        print("Error: ", error)

        conn.rollback()
   


while True:
    try:
        conn_string()
        
        #Define our connection string
        # conn_string = Settings.database_string
        # conn_string = "host='10.0.52.89' port='5432' dbname='sinfordb' user='DtS28Hbfac' password='qlS8mYmDUnsKXJflZDM7FouCLDWYpEiV'"

        # print the connection string we will use to connect
        # print ("Connecting to database\n	->%s" % (conn_string))

        # get a connection, if a connect cannot be made an exception will be raised here
        # conn = psycopg2.connect(conn_string, cursor_factory=RealDictCursor)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        # cursor = conn.cursor()
        # print("Database connected!\n")
        break
    except Exception as error:
        print("Connection failed")
        print("Error: ", error)
        time.sleep(2)