# app/__init__.py

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
import os
from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_sse import sse
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'None'
login_manager.login_view = 'auth.login'
images = UploadSet('images', IMAGES)
csrf = CSRFProtect()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app._static_folder = os.path.abspath("static/")
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    # blueprint registration
    return app
