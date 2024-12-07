from sqlalchemy import (
    Column,
    String,
)

from app.infra.db import Base


class Categoria(Base):
    nome = Column(String(40), nullable=False)


