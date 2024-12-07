import os
from functools import lru_cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker


@lru_cache
def get_engine() -> Engine:
    return create_engine(str(os.getenv("DB_URL")))


@lru_cache
def get_session() -> scoped_session[Session]:
    db_session = scoped_session(sessionmaker(bind=get_engine()))
    return db_session
