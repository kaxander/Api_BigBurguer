from typer import Typer

from app.config import get_settings
from app.product.command import app as product_cmd


def create_app() -> Typer:
    config = get_settings()
    app = Typer(name=config.title, help=config.description)
    app.add_typer(product_cmd)

    return app
