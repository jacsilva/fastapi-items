from typing import Union, List

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


# request method GET latest item
# @app.get("/items/latest")
# def get_latest_item():
#     item = my_items[len(my_items)-1]
#     return {"detail": item}



#------------   C   R   U   D  : Items   ---------------------#

# request method POST create items
@app.post("/items", status_code=status.HTTP_201_CREATED, response_model=schemas.Item)
def create_item(item: schemas.CreateItems, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_title(models=models.DocsModelAdm, db=db, title=item.title)
    if db_item:
        raise HTTPException(status_code=400, detail=f"Item com o título '{item.title}' já existe!")

    return crud.create_item(db, item)
  
  
# request method GET read item ID
@app.get("/items/{id}", response_model=schemas.Item)
def read_item(id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_id(models=models.DocsModelAdm, db=db, id=id)
   
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item com id: {id} não existe.")
    return db_item


# request method PUT update item ID
@app.put('/items/{id}', response_model=schemas.Item)
def update_item(id: int, updated_schemas: schemas.UpdateItems, db: Session = Depends(get_db)):
    db_item = crud.get_item_for_delete_or_update(models=models.DocsModelAdm, db=db, id=id)

    if db_item.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item com id: {id} não existe.")
    updated_item = crud.update_item(db_item, db, updated_schemas)
    
    return updated_item   


# request method DELETE delete item ID
@app.delete("/items/{id}")
def delete_item(id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item_for_delete_or_update(models=models.DocsModelAdm, db=db, id=id)
    if db_item.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item com id: {id} não existe.")
    db_item = crud.delete_item(db_item, db)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# request method GET list items
@app.get("/items", response_model=List[schemas.Item])
def list_items(db: Session = Depends(get_db), skip: int = 0, limit: int = 10,):
    docs = crud.get_items_all(db, skip=skip, limit=limit)
    return docs





#------------   C   R   U   D  : Groups   ---------------------#

# request method POST create groups
@app.post("/groups", status_code=status.HTTP_201_CREATED)
def create_group(item: schemas.CreateGroups, db: Session = Depends(get_db)):
    db_group = crud.get_item_by_title(models=models.DocsModelGroup, db=db, title=item.title)
    if db_group:
        raise HTTPException(status_code=400, detail=f"Grupo com o nome '{item.title}' já existe!")

    db_group = crud.create_group(db, item) 
    return {"data": db_group}