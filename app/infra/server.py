from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from app.infra.db import Base, get_engine


def show_docs(request: Request):
    return f"{request.base_url}docs"


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.get("/", response_class=RedirectResponse, include_in_schema=False)(show_docs)
    Base.metadata.create_all(get_engine())
    yield

