from sqlalchemy import (
    Column,
    String,
)

from app.infra.db import Base


class Funcionario(Base):

    nome = Column(String(40), nullable=False)
    email = Column(String(40), nullable=False, unique=True)
    senha = Column(String(40), nullable=False)
    telefone = Column(String(40), nullable=False, unique=True)

