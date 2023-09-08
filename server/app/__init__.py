# /app/__init__.py

from flask import Flask
from flask_mongoengine import MongoEngine

db = MongoEngine()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    from .views import urls_bp
    app.register_blueprint(urls_bp)

    from .views import gsb_bp
    app.register_blueprint(gsb_bp)

    return app