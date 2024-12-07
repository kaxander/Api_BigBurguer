from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import relationship

from app.infra.db import Base


class PedidoProduto(Base):
    produto_id = Column(Integer, ForeignKey("produto.id"))
    pedido_id = Column(Integer, ForeignKey("pedido.id"))
    quantidade = Column(Integer, nullable=False, default=1)

    relationship("Produto")
    relationship("Pedido")
