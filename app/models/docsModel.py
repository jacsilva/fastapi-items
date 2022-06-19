from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
import sqlalchemy.types as types

from app.database import Base


class ChoiceType(types.TypeDecorator):

    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.iteritems() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]


class DocsModelAdm(Base):
    __tablename__ = "docsadm"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    status = Column(
            ChoiceType({"RECEBIDO": "RECEBIDO", "ENCAMINHADO": "ENCAMINHADO", "EM EXECUÇÃO": "EM EXECUÇÃO", "EM ENCERRADO": "EM ENCERRADO"}), nullable=True
        )
    group_id = Column(Integer, ForeignKey("docsgroup.id"), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class DocsModelGroup(Base):
    __tablename__ = "docsgroup"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)


