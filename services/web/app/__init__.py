import os
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, Flask
from config import config
from dbUtils import metadata

db = SQLAlchemy(metadata=metadata)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)
    return app
