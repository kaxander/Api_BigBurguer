
if __name__ == "__main__":
    from app.cli import create_app

    app = create_app()
    app()


else:
    from app.asgi import create_app

    app = create_app()
