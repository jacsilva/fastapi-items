from sqlalchemy.orm import Session

from . import models, schemas


def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.DocsModelAdm).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.CreateItems):
    db_docs = models.DocsModelAdm(
        title=item.title, content=item.content
        )
    db.add(db_docs)
    db.commit()
    db.refresh(db_docs)
    return db_docs

def get_item_by_title(db: Session, title: str):
    return db.query(models.DocsModelAdm).filter(models.DocsModelAdm.title == title).first()