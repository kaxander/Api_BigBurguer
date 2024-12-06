from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

cors_config = {
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True,
    }
}

load_dotenv()


def create_app():
    from app.command import app as command
    from app.controller import app as router

    app = Flask(__name__)
    CORS(app, resources=cors_config)
    app.register_blueprint(router)
    app.register_blueprint(command)

    return app
