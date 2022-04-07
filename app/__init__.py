# app/__init__.py
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
import os,time
from datetime import datetime, timedelta
from calendar import week
from adbutils import device
from flask_babel import Babel

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
from .models import Device_Data , Device_Info , User_Mgmt



def get_yesterdaygeneratedElectricity(uuid):
    model='Delta_RPI-M10A'
    scope='generatedElectricity'
    etime = int(datetime.now().replace(hour=0,minute=0,second=0,microsecond=0).timestamp()-3600*8)*1000
    stime = etime - 86400000 - 3600000 * 8
    devicedata = Device_Data.getyesterday(uuid,model,scope,stime,etime).first()
    
    if devicedata:
        return(round(devicedata.value, 1))
    #if empty return 0
    else:
        return(0)

def get_generatedElectricity(uuid):
    model='Delta_RPI-M10A'
    scope='generatedElectricity'
    time = int(datetime.now().replace(hour=0,minute=0,second=0,microsecond=0).timestamp())*1000
    devicedata = Device_Data.gettoday(uuid,model,scope,time).first()
    
    if devicedata:
        return(round(devicedata.value, 1))
    #if empty return 0
    else:
        return(0)

def get_weeklygenElec(device):
    # Assuming that a week starts from monday
    model='Delta_RPI-M10A'
    scope='generatedElectricity'
    time = int(datetime.now().timestamp()-1800)*1000
    devicedata = Device_Data.gettoday(device.uuid,model,scope,time).first()
    #     now_time = datetime.now()
    #     prev_monday = now_time - timedelta(days=now_time.weekday())
    #     start_time = int(prev_monday.replace(hour=0,minute=0,second=0,microsecond=0).timestamp())*1000
    #     end_time = start_time + 86400000
    #     max_time = int(now_time.replace(hour=0,minute=0,second=0,microsecond=0).timestamp())*1000+86400000
    #     week_sum = 0
    #     while end_time <= max_time :
    #         if Device_Data.getyesterday(device.uuid,model,scope,start_time,end_time).first():
    #             week_sum += Device_Data.getyesterday(device.uuid,model,scope,start_time,end_time).first().value
    #         end_time += 86400000
    #         start_time += 86400000
    if devicedata:
        return(round(device.weekly_energy_amount+devicedata.value, 1))
    return(round(device.weekly_energy_amount, 1))
    
def get_monthlygenElec(device):
    #     firstDayofMonth = datetime.today().replace(day=1)
    #     start_time = int(firstDayofMonth.replace(hour=0,minute=0,second=0,microsecond=0).timestamp())*1000
    #     end_time = start_time + 86400000
    #     max_time = int(datetime.now().replace(hour=0,minute=0,second=0,microsecond=0).timestamp())*1000+86400000
    #     month_sum = 0
    #     while end_time <= max_time :
    #         if Device_Data.getyesterday(device.uuid,model,scope,start_time,end_time).first():
    #             month_sum += Device_Data.getyesterday(device.uuid,model,scope,start_time,end_time).first().value
    #         end_time += 86400000
    #         start_time += 86400000
    #     return(round(month_sum, 1))
    model='Delta_RPI-M10A'
    scope='generatedElectricity'
    time = int(datetime.now().timestamp()-1800)*1000
    devicedata = Device_Data.gettoday(device.uuid,model,scope,time).first()
    if devicedata:
        return(round(device.monthly_energy_amount+devicedata.value, 1))
    return(round(device.monthly_energy_amount, 1))

def get_instanceElectricity(uuid):
    model='Delta_RPI-M10A'
    scope='instanceElectricity'
    time = int(datetime.now().timestamp()-1800)*1000
    devicedata = Device_Data.gettoday(uuid,model,scope,time).first()
    
    if devicedata:
        return(round(devicedata.value, 3))
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

def get_grpLowerBound(device):
    if device.group_id != '0':
        return str(device.group_lower_bound) +" W"
    return "未加入任何群組"



    
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    app._static_folder = os.path.abspath("static/")
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    babel = Babel(app)
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    app.jinja_env.globals.update(get_instanceElectricity=get_instanceElectricity)
    app.jinja_env.globals.update(get_generatedElectricity=get_generatedElectricity)
    app.jinja_env.globals.update(get_yesterdaygeneratedElectricity=get_yesterdaygeneratedElectricity)
    app.jinja_env.globals.update(get_weeklygenElec=get_weeklygenElec)
    app.jinja_env.globals.update(get_monthlygenElec=get_monthlygenElec)
    app.jinja_env.globals.update(no_device=no_device)
    app.jinja_env.globals.update(display_device_name=display_device_name)
    app.jinja_env.globals.update(get_grpLowerBound=get_grpLowerBound)
    return app
