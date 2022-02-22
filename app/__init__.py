# app/__init__.py
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
import os,time
from datetime import datetime

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
from .models import Device_Data , Device_Info , User_Mgmt


def get_yesterdaygeneratedElectricity(uuid):
    model='Delta_RPI-M10A'
    scope='generatedElectricity'
    stime = int(datetime.now().timestamp()-24*60*60)*1000
    etime = int(datetime.now().replace(hour=0,minute=0,second=0,microsecond=0).timestamp()-8*3600)*1000
    devicedata = Device_Data.getyesterday(uuid,model,scope,stime,etime).first()
    
    if devicedata:
        return(devicedata.value)
    #if empty return 0
    else:
        return(0)

def get_generatedElectricity(uuid):
    model='Delta_RPI-M10A'
    scope='generatedElectricity'
    time = int(datetime.now().replace(hour=0,minute=0,second=0,microsecond=0).timestamp())*1000
    devicedata = Device_Data.gettoday(uuid,model,scope,time).first()
    
    if devicedata:
        return(devicedata.value)
    #if empty return 0
    else:
        return(0)

def get_instanceElectricity(uuid):
    model='Delta_RPI-M10A'
    scope='instanceElectricity'
    time = int(datetime.now().timestamp()-1800)*1000
    devicedata = Device_Data.gettoday(uuid,model,scope,time).first()
    
    if devicedata:
        return(devicedata.value)
    #if empty return 0
    else:
        return(0)
    
def no_device(list):
    count = False
    for device in list: 
        if device.model == 'Delta_RPI-M10A' :
            count = True
    return count

def display_device_name(device):
    if device.group_id != '0':
        return "群組"+device.group_id+"："+device.name
    return device.name
    
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    app._static_folder = os.path.abspath("static/")
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    app.jinja_env.globals.update(get_instanceElectricity=get_instanceElectricity)
    app.jinja_env.globals.update(get_generatedElectricity=get_generatedElectricity)
    app.jinja_env.globals.update(get_yesterdaygeneratedElectricity=get_yesterdaygeneratedElectricity)
    app.jinja_env.globals.update(no_device=no_device)
    app.jinja_env.globals.update(display_device_name=display_device_name)
    return app