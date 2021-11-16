# app/__init__.py
# app/__init__.py

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
import os
bootstrap = Bootstrap()
moment = Moment()

def create_app(config_name):
    app = Flask(__name__)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    bootstrap.init_app(app)
    moment.init_app(app)
    return app