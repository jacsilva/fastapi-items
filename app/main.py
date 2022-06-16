from typing import Union

from fastapi import FastAPI, HTTPException, status
from fastapi.params import Body
from models import CreateItems
from random import randrange

app = FastAPI()

my_items = [
    {'id': 1, 'title': 'django, o filme', 'content': 'conteúdo django', 'published': True, 'rating': 2},
    {'id': 2, 'title': 'fast, a api', 'content': 'conteúdo fast', 'published': False, 'rating': 3}
]



@app.get("/")
def read_root():
    return {"Hello": "World"}


# request method POST items
@app.post("/createitems", status_code=status.HTTP_201_CREATED)
def create_items(new_item: CreateItems):
    # print(new_item.dict())
    item_dict = new_item.dict()
    item_dict['id'] = randrange(0, 1000000)
    my_items.append(item_dict)
    return {"new_item": f"Novo item criado: {item_dict['title'], item_dict['id']}"}


# request method GET items
@app.get("/items")
def get_items():
    return {"data": my_items}


# request latest item
@app.get("/items/latest")
def get_latest_item():
    item = my_items[len(my_items)-1]
    return {"detail": item}


def find_item(id):
    for it in my_items:
        if it['id'] == id:
            return it


# request method GET item ID
@app.get("/items/{id}")
def get_item(id: int):
    item = find_item(id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item com id: {id} não encontrado.")
    return {"item_detail": item}


# request method GET item ID
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# request method PUT item ID

# request method DELETE item ID