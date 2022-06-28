from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from sqlalchemy.orm import Session

from ..models import docs_model
from ..schemas import docs_schema

from ..database import engine, get_db
from .. import crud

docs_model.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/groups",
    tags=["Groups"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)



#------------   C   R   U   D  : Groups   ---------------------#

# request method POST create groups
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_group(item: docs_schema.CreateGroups, db: Session = Depends(get_db)):
    db_group = crud.get_item_by_title(model=docs_model.DocsModelGroup, db=db, title=item.title)
    if db_group:
        raise HTTPException(status_code=400, detail=f"Grupo com o nome '{item.title}' já existe!")

    db_group = crud.create_group(db, item) 
    return {"data": db_group}


# request method GET list groups
@router.get("/", response_model=List[docs_schema.Group])
def list_items(db: Session = Depends(get_db), skip: int = 0, limit: int = 10,):
    docs = crud.get_items_all(docs_model.DocsModelGroup, db, skip=skip, limit=limit)
    return docs