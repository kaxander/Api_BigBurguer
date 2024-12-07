from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.infra.db import Base


class Produto(Base):
    nome = Column(String(40), nullable=False)
    descricao = Column(String(40), nullable=False)
    imagem = Column(String(40), nullable=False)
    preco = Column(Float, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categoria.id"))

    relationship("Categoria")
