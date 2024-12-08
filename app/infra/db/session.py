from functools import lru_cache
from typing import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings


def get_engine() -> Engine:
    config = get_settings()
    return create_engine(config.db_url)


@lru_cache
def session_maker() -> sessionmaker[Session]:
    return sessionmaker(get_engine())


def get_session() -> Generator[Session, None, None]:
    SessionLocal = session_maker()
    with SessionLocal() as session:
        yield session
