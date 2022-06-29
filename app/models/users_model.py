from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
import sqlalchemy.types as types
from sqlalchemy_utils.types.choice import ChoiceType
from sqlalchemy.orm import relationship

from app.database import Base
 
    

class User(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True, index=True) 
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, unique=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    

