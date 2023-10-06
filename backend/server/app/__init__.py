# /app/__init__.py

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_cors import CORS

db = MongoEngine()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    CORS(app)

    from .views import urls_bp
    app.register_blueprint(urls_bp)

    from .views import processing_bp
    app.register_blueprint(processing_bp)

    return app