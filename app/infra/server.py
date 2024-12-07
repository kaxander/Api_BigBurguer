from contextlib import asynccontextmanager

import alembic.config
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse


def show_docs(request: Request):
    return f"{request.base_url}docs"


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.get("/", response_class=RedirectResponse, include_in_schema=False)(show_docs)
    alembicArgs = [
        '--raiseerr',
        'upgrade', 'head',
    ]
    alembic.config.main(argv=alembicArgs)
    yield

