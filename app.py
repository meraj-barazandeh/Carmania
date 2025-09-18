from flask import Flask
from database import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from routes.auth import auth_bp
from routes.cars import cars_bp
from routes.service import service_bp
import os
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///carmania.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default-secret-key")

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    # Blueprint
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(cars_bp, url_prefix="/cars")
    app.register_blueprint(service_bp, url_prefix="/service")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
