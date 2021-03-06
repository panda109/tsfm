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
import requests

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
from .models import Device_Data , Device_Info , User_Mgmt


def get_gwname(uuid):
    token='qt5pOgkyHX3SqxqzfvN/ADVAg3KbV5zrWIXbM8H'
    qa_std = "https://ioeapi-qa.nextdrive.io/v2/gateways/"+ uuid +"/status"

    headers = {'Accept': 'application/json' , 'X-ND-TOKEN' : token}
    r = requests.get(qa_std , headers = headers )
    #print(r.text)
    return(r.json()['name'])

def get_yesterdaygeneratedElectricity(uuid):

    scope='generatedElectricity'
    etime = int(datetime.now().replace(hour=0,minute=0,second=0,microsecond=0).timestamp()-3600*8)*1000
    stime = etime - 86400000 - 3600000 * 8
    devicedata = Device_Data.getyesterday(uuid,scope,stime,etime).first()
    
    if devicedata:
        return(round(devicedata.value, 1))
    #if empty return 0
    else:
        return(0)

def get_generatedElectricity(uuid):
    scope='generatedElectricity'
    time = int(datetime.now().replace(hour=0,minute=0,second=0,microsecond=0).timestamp())*1000
    devicedata = Device_Data.gettoday(uuid,scope,time).first()
    
    if devicedata:
        return(round(devicedata.value, 1))
    #if empty return 0
    else:
        return(0)

def get_weeklygenElec(device):
    # Assuming that a week starts from monday
    scope='generatedElectricity'
    time = int(datetime.now().timestamp()-1800)*1000
    devicedata = Device_Data.gettoday(device.uuid,scope,time).first()
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
    scope='generatedElectricity'
    time = int(datetime.now().timestamp()-1800)*1000
    devicedata = Device_Data.gettoday(device.uuid,scope,time).first()
    if devicedata:
        return(round(device.monthly_energy_amount+devicedata.value, 1))
    return(round(device.monthly_energy_amount, 1))

def get_annualgenElec(device):
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
    scope='generatedElectricity'
    time = int(datetime.now().timestamp()-1800)*1000
    devicedata = Device_Data.gettoday(device.uuid,scope,time).first()
    if devicedata:
        return(round(device.annual_energy_amount+devicedata.value, 1))
    return(round(device.annual_energy_amount, 1))

def get_instanceElectricity(uuid):
    scope='instanceElectricity'
    time = int(datetime.now().timestamp()-1800)*1000
    devicedata = Device_Data.gettoday(uuid,scope,time).first()
    
    if devicedata:
        return(round(devicedata.value, 3))
    #if empty return 0
    else:
        return(0)
    
def no_device(list):
    count = False
    for device in list: 
        if device.model :
            count = True
    return count

def display_device_name(device):
    if device.group_id != '0':
        return "??????"+device.group_id+"???"+device.name
    return device.name

def get_grpLowerBound(device):
    if device.group_id != '0':
        return str(device.group_lower_bound) +" W"
    return "?????????????????????"
    
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
    app.jinja_env.globals.update(get_weeklygenElec=get_weeklygenElec)
    app.jinja_env.globals.update(get_monthlygenElec=get_monthlygenElec)
    app.jinja_env.globals.update(get_annualgenElec=get_annualgenElec)
    app.jinja_env.globals.update(no_device=no_device)
    app.jinja_env.globals.update(display_device_name=display_device_name)
    app.jinja_env.globals.update(get_grpLowerBound=get_grpLowerBound)
    app.jinja_env.globals.update(get_gwname=get_gwname)
    return app