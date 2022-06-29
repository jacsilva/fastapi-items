from sqlalchemy.orm import Session



def get_items_all(model, db: Session, skip: int = 0, limit: int = 10):
    return db.query(model).offset(skip).limit(limit).all()


def create_item(db: Session, model, schema):
    db_docs = model(**schema.dict())
    db.add(db_docs)
    db.commit()
    db.refresh(db_docs) 
    return db_docs


def delete_item(db_item, db: Session):
    db_item.delete(synchronize_session=False)
    db.commit()
    return db_item.first()
    

def update_item(db_item, db: Session, updated_item):
    db_item.update(updated_item.dict(), synchronize_session=False)
    db.commit()
    print(updated_item.dict())
    return db_item.first()


def get_item_by_title(model, db: Session, title: str):
    return db.query(model).filter(model.title == title).first()


def get_item_by_id(model, db: Session, id: int):
    return db.query(model).filter(model.id == id).first()


def get_item_for_delete_or_update(model, db: Session, id: int):
    return db.query(model).filter(model.id == id)


def verify_if_user_exist(model, db: Session, schema):
    username = db.query(model).filter(model.username == schema.username).first()
    email = db.query(model).filter(model.email == schema.email).first()
    if username or email:
        return True
    else:
        return False

