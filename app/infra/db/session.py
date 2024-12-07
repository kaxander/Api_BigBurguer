from functools import lru_cache
from typing import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings


def get_engine() -> Engine:
    config = get_settings()
    return create_engine(config.db_url)


@lru_cache
def get_sessionmaker() -> sessionmaker[Session]:
    return sessionmaker(get_engine())


def get_session() -> Generator[Session, None, None]:
    create_session = get_sessionmaker()
    with create_session() as session:
        yield session
