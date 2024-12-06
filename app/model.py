#importar bibliotecas
import os
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, scoped_session, sessionmaker

engine = create_engine(str(os.getenv("DB_URL")))

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def create_database():
    Base.metadata.create_all(bind=engine)


class Categoria(Base):
    __tablename__ = 'categoria'
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        dados_categoria = {
            'id': self.id,
            'nome': self.nome,
        }
        return dados_categoria


class Funcionario(Base):
    __tablename__ = 'funcionario'
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False)
    email = Column(String(40), nullable=False, unique=True)
    senha = Column(String(40), nullable=False)
    telefone = Column(String(40), nullable=False, unique=True)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        dados_funcionario = {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha,
            'telefone': self.telefone,
        }
        return dados_funcionario

class Produto(Base):
    __tablename__ = 'produto'
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False)
    descricao = Column(String(40), nullable=False)
    imagem = Column(String(40), nullable=False)
    preco = Column(Float, nullable=False)
    categoria_id = Column(Integer, ForeignKey('categoria.id'))

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        dados_produto = {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'imagem': self.imagem,
            'preco': self.preco,
            'categoria_id': self.categoria_id,
        }
        return dados_produto

# Definição do Enum Python para o status
class StatusPedido(PyEnum):
    PENDENTE = "PENDENTE"
    EM_ESPERA = "EM_ESPERA"
    EM_PRODUCAO = "EM_PRODUCAO"
    FINALIZADO = "FINALIZADO"

class Pedido(Base):
    __tablename__ = 'pedido'
    id = Column(Integer, primary_key=True)
    mesa = Column(String(10), nullable=False)
    status = Column(Enum(StatusPedido), nullable=False, default=StatusPedido.EM_ESPERA)
    dataCriado = Column(DateTime)
    funcionario_id = Column(Integer, ForeignKey('funcionario.id'))
    relationship(Funcionario)

    def save(self):
        if not self.dataCriado:
            self.dataCriado = datetime.now()
        db_session.add(self)
        db_session.commit()

    def serialize(self):
        dados_pedido = {
            'id': self.id,
            'mesa': self.mesa,
            'status': self.status.value,
            'dataCriado': self.dataCriado.strftime("%d/%m/%Y %H:%M:%S") if self.dataCriado else None,
            'funcionario_id': self.funcionario_id
        }
        return dados_pedido


class PedidoProduto(Base):
    __tablename__ = 'pedidoproduto'
    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey('produto.id'))
    relationship(Produto)
    pedido_id = Column(Integer, ForeignKey('pedido.id'))
    relationship(Pedido)
    quantidade = Column(Integer, nullable=False, default=1)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        dados_pedidoProduto = {
            'id': self.id,
            'produto_id': self.produto_id,
            'pedido_id': self.pedido_id,
            'quantidade': self.quantidade,
        }
        return dados_pedidoProduto


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
