from fastapi import APIRouter, Response, HTTPException, status, Depends
from typing import List

from sqlalchemy.orm import Session

from ..models import docs_model
from ..schemas import docs_schema

from ..database import engine, get_db
from .. import crud

docs_model.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/items",
    tags=["Items"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


#------------   C   R   U   D  : Items   ---------------------#

# request method POST create items
@router.post("/{group_id}/items", status_code=status.HTTP_201_CREATED, response_model=docs_schema.Item)
def create_item(group_id: int, item: docs_schema.CreateItems, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_title(model=docs_model.DocsModelAdm, db=db, title=item.title)
    print(group_id)
    if db_item:
        raise HTTPException(status_code=400, detail=f"Item com o título '{item.title}' já existe!")

    return crud.create_item(db, item, id_group=group_id)
  
  
# request method GET read item ID
@router.get("/{id}", response_model=docs_schema.Item)
def read_item(id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_id(model=docs_model.DocsModelAdm, db=db, id=id)
    print(db_item.status)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item com id: {id} não existe.")
    return db_item


# request method PUT update item ID
@router.put('/{id}', response_model=docs_schema.Item)
def update_item(id: int, updated_schemas: docs_schema.UpdateItems, db: Session = Depends(get_db)):
    db_item = crud.get_item_for_delete_or_update(model=docs_model.DocsModelAdm, db=db, id=id)

    if db_item.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item com id: {id} não existe.")
    updated_item = crud.update_item(db_item, db, updated_schemas)
    
    return updated_item   


# request method DELETE delete item ID
@router.delete("/{id}")
def delete_item(id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item_for_delete_or_update(model=docs_model.DocsModelAdm, db=db, id=id)
    if db_item.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item com id: {id} não existe.")
    db_item = crud.delete_item(db_item, db)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# request method GET list items
@router.get("/", response_model=List[docs_schema.Item])
def list_items(db: Session = Depends(get_db), skip: int = 0, limit: int = 10,):
    docs = crud.get_items_all(docs_model.DocsModelAdm, db, skip=skip, limit=limit)
    return docs

