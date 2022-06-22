from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
import sqlalchemy.types as types
from sqlalchemy_utils.types.choice import ChoiceType

from app.database import Base


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
    group_id = Column(Integer, ForeignKey("docsgroup.id"), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))  


class DocsModelGroup(Base):
    __tablename__ = "docsgroup"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)


