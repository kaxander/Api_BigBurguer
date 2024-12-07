from old.enum import StatusPedidoEnum
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.infra.db import Base


class Pedido(Base):
    mesa = Column(String(10), nullable=False)
    status = Column(
        Enum(StatusPedidoEnum), nullable=False, default=StatusPedidoEnum.EM_ESPERA
    )
    dataCriado = Column(DateTime)
    funcionario_id = Column(Integer, ForeignKey("funcionario.id"))

    relationship("Funcionario")
