# coding: utf-8
from flask import Flask
from flask_cors import CORS
from app.configFiles.sqlConfig import SQLCONFIG
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(SQLCONFIG)

    db.init_app(app)

    from .emqx import emqx as emqx_blueprint
    app.register_blueprint(emqx_blueprint, url_prefix='/api/emqx')

    return app
