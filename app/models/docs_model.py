from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
import sqlalchemy.types as types
from sqlalchemy_utils.types.choice import ChoiceType
from sqlalchemy.orm import relationship

from app.database import Base


class DocsModelGroup(Base):
    __tablename__ = "docsgroup"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)

    items = relationship("DocsModelAdm", back_populates="group")


class DocsModelAdm(Base):
    __tablename__ = "docsadm"

    STATUS_TYPES = [
        (1, "RECEBIDO"), 
        (2, "ENCAMINHADO"), 
        (3, "EM EXECUÇÃO"), 
        (4, "ENCERRADO") 
    ]

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False) 
    content = Column(String, nullable=False)
    status = Column(
            ChoiceType(STATUS_TYPES, impl=Integer()), nullable=True
        )
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))  
    group_id = Column(Integer, ForeignKey("docsgroup.id"), nullable=True)

    group = relationship("DocsModelGroup", back_populates="items")


    

class User(Base):
    __tablename__="User"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    

