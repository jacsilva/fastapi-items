from fastapi import APIRouter, HTTPException, Response, status, Depends
from typing import List

from sqlalchemy.orm import Session

from ..models import groups_model
from ..schemas import groups_schemas

from ..database import engine, get_db
from .. import crud

groups_model.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/groups",
    tags=["Groups"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)



#------------   C   R   U   D  : Groups   ---------------------#

# request method POST create groups
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_group(schema: groups_schemas.CreateGroups, db: Session = Depends(get_db)):
    model=groups_model.DocsModelGroup
    db_group = crud.get_item_by_title(model=model, db=db, title=schema.title)
    if db_group:
        raise HTTPException(status_code=400, detail=f"Grupo com o nome '{schema.title}' já existe!")

    crud.create_item(db=db, model=model, schema=schema)
    return { "detail": f"Grupo '{schema.title}' criado com sucesso!"}


# request method GET read group ID
@router.get("/{id}", response_model=groups_schemas.Group)
def read_group(id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_id(model=groups_model.DocsModelGroup, db=db, id=id)
    
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Grupo com id: {id} não existe.")
    return db_item


# request method GET list groups
@router.get("/", response_model=List[groups_schemas.Group])
def list_items(db: Session = Depends(get_db), skip: int = 0, limit: int = 10,):
    docs = crud.get_items_all(groups_model.DocsModelGroup, db, skip=skip, limit=limit)
    return docs