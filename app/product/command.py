from rich.console import Console
from rich.table import Table
from typer import Typer

from app.infra.db import session_maker
from app.product import service as product_service

app = Typer(name="product")
console = Console()
SessionLocal = session_maker()


@app.command(name="get_all")
def get_all_products():
    with SessionLocal() as session:
        products = product_service.get_products(session=session)
        if not products:
            console.print("Products not found!")
        else:
            table = Table(title="Product")
            for idx, product in enumerate(products):
                p = product.model_dump(mode="json")
                if idx == 0:
                    for key in p.keys():
                        table.add_column(key)
                table.add_row(*[str(v) for v in p.values()])
            console.print(table)
