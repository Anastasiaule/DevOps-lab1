from flask import Flask
from .database import init_app, create_tables


def create_app():
    app = Flask(__name__)

    app.config["TESTING"] = False
    app.config["DATABASE"] = "library.db"

    init_app(app)

    from .routes import register_routes
    register_routes(app)

    with app.app_context():
        create_tables()

    return app