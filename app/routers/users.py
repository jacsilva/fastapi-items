from fastapi import APIRouter, HTTPException, Response, status, Depends
from typing import List

from sqlalchemy.orm import Session

from ..models import users_model
from ..schemas import users_schemas

from ..database import engine, get_db
from .. import crud, utils

users_model.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
 


#------------   C   R   U   D  : Groups   ---------------------#

# request method POST create groups
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(schema: users_schemas.UserCreate  , db: Session = Depends(get_db)):
    model=users_model.User
    db_user = crud.verify_if_user_exist(model=model, db=db, schema=schema)
    if db_user:
        raise HTTPException(status_code=400, detail=f"Usuário '{schema.username}' já existe!")

    hashed_password = utils.get_password_hash(schema.password)
    schema.password = hashed_password

    crud.create_item(db=db, model=model, schema=schema)
    return { "detail": f"Usuário '{schema.username}' criado com sucesso!"}


# request method GET read user ID
@router.get("/{id}", response_model=users_schemas.User)
def read_user(id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_id(model=users_model.User, db=db, id=id)
    
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Usuários com id: {id} não existe.")
    return db_item


# request method DELETE delete item ID
@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item_for_delete_or_update(model=users_model.User, db=db, id=id)
    if db_item.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Usuário com id: {id} não existe.")
    db_item = crud.delete_item(db_item, db)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# request method GET list users
@router.get("/", response_model=List[users_schemas.User])
def list_items(db: Session = Depends(get_db), skip: int = 0, limit: int = 10,):
    docs = crud.get_items_all(users_model.User, db, skip=skip, limit=limit)
    return docs