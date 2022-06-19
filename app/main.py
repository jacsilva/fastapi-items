from typing import Union

from fastapi import FastAPI, Response, HTTPException, status, Depends
from fastapi.params import Body
# from app.models.createitem import CreateItems
from random import randrange

from . import config

from .models import docsModel
from .database import engine, get_db
from sqlalchemy.orm import Session

docsModel.Base.metadata.create_all(bind=engine)


app = FastAPI()




my_items = [
    {'id': 1, 'title': 'django, o filme', 'content': 'conteúdo django', 'published': True, 'rating': 2},
    {'id': 2, 'title': 'fast, a api', 'content': 'conteúdo fast', 'published': False, 'rating': 3}
]


@app.get("/info")
async def info(settings = Depends(config.get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.database_string,
    }

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/posts/")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}


# request method GET list items
@app.get("/items")
def list_items():
    return {"data": my_items}


# request method GET latest item
@app.get("/items/latest")
def get_latest_item():
    item = my_items[len(my_items)-1]
    return {"detail": item}


# request method POST create items
# @app.post("/items", status_code=status.HTTP_201_CREATED)
# def create_item(new_item: CreateItems):
#     # print(new_item.dict())
#     item_dict = new_item.dict()
#     item_dict['id'] = randrange(0, 1000000)
#     my_items.append(item_dict)
#     return {"new_item": f"Novo item criado: {item_dict['title'], item_dict['id']}"}


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

    
# request method GET item ID
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# request method PUT update item ID
@app.put('/items/{id}')
# def update_item(id: int, item: CreateItems):
#     index = find_index_item(id)

#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Item com id: {id} não existe.")
    
#     item_dict = item.dict()
#     item_dict['id'] = id
#     my_items[index] = item_dict

#     return {'data': item_dict}


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


