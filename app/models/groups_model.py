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
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    items = relationship("DocsModelAdm", back_populates="group")



