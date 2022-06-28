from sqlalchemy.orm import Session

from .models import docs_model
from .schemas import docs_schema


def get_items_all(model, db: Session, skip: int = 0, limit: int = 10):
    return db.query(model).offset(skip).limit(limit).all()


def create_item(db: Session, item: docs_schema.CreateItems):
    db_docs = docs_model.DocsModelAdm(**item.dict())
    # db_docs = docs_model.DocsModelAdm(**item.dict(), group_id=item.group_id)
    db.add(db_docs)
    db.commit()
    db.refresh(db_docs)
    return db_docs


def create_group(db: Session, item: docs_schema.CreateGroups):
    db_groups = docs_model.DocsModelGroup(
        title = item.title
    )
    db.add(db_groups)
    db.commit()
    db.refresh(db_groups)
    return db_groups


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


