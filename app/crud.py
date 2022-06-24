from sqlalchemy.orm import Session

from . import models, schemas


def get_items_all(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.DocsModelAdm).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.CreateItems):
    db_docs = models.DocsModelAdm(
        title=item.title, content=item.content
        )
    db.add(db_docs)
    db.commit()
    db.refresh(db_docs)
    return db_docs


def create_group(db: Session, item: schemas.CreateGroups):
    db_groups = models.DocsModelGroup(
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
    return db_item.first()


def get_item_by_title(models: models, db: Session, title: str):
    return db.query(models).filter(models.title == title).first()


def get_item_by_id(models: models, db: Session, id: int):
    return db.query(models).filter(models.id == id).first()


def get_item_for_delete_or_update(models: models, db: Session, id: int):
    return db.query(models).filter(models.id == id)


