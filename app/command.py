
from flask import Blueprint

app = Blueprint("db", __name__)

@app.cli.command('create')
def create():
    from app import model
    
    model.create_database()

