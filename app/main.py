from typing import Union

from fastapi import FastAPI, Response, HTTPException, status, Depends
from fastapi.params import Body
from random import randrange
from sqlalchemy.orm import Session

from . import config, schemas, models, crud

from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


my_items = [
    {'id': 1, 'title': 'django, o filme', 'content': 'conteúdo django', 'published': True, 'rating': 2},
    {'id': 2, 'title': 'fast, a api', 'content': 'conteúdo fast', 'published': False, 'rating': 3}
]


@app.get("/info")
async def get_info(settings = Depends(config.get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.database_string,
    }

@app.get("/")
def read_root():
    return {"Hello": "World"}


# request method GET list items
@app.get("/items")
def list_items(db: Session = Depends(get_db), skip: int = 0, limit: int = 10,):
    docs = crud.get_items(db, skip=skip, limit=limit)
    return {"data": docs}


# request method GET latest item
@app.get("/items/latest")
def get_latest_item():
    item = my_items[len(my_items)-1]
    return {"detail": item}


# request method POST create items
@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: schemas.CreateItems, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_title(db, title=item.title)
    if db_item:
        raise HTTPException(status_code=400, detail=f"Item com o título '{item.title}' já existe!")

    db_item = crud.create_item(db, item)
    return {"data": db_item}
    # return {"new_item": f"Novo item criado: {item_dict['title'], item_dict['id']}"}


# request method GET read item ID
def find_item(id):
    for it in my_items:
        if it['id'] == id:
            return it


@app.get("/items/{id}")
def read_item(id: int):
    item = find_item(id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item com id: {id} não existe.")
    return {"item_detail": item}


# request method PUT update item ID
@app.put('/items/{id}')
def update_item(id: int, item: schemas.CreateItems):
    index = find_index_item(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item com id: {id} não existe.")
    
    item_dict = item.dict()
    item_dict['id'] = id
    my_items[index] = item_dict

    return {'data': item_dict}


# request method DELETE delete item ID
def find_index_item(id):
    for i, t in enumerate(my_items):
        if t['id'] == id:
            return i

@app.delete("/items/{id}")
def delete_item(id: int):
    index = find_index_item(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item com id: {id} não existe.")
    my_items.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


