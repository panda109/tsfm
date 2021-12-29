# app/models.py

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

#add JsonEncodedDict support
#from app.JsonEncodedDict import JsonEncodedDict
    
class Device_Data(UserMixin, db.Model):
    __tablename__ = 'device_data'
    id = db.Column(db.Integer, primary_key=True)
    dev_uuid = db.Column(db.String(64), index = True)
    scope = db.Column(db.String(64))
    model = db.Column(db.String(64))
    value = db.Column(db.Float)
    generated_time = db.Column(db.BigInteger)
    uploaded_time = db.Column(db.BigInteger)

    def __repr__(self):
        return "<Device Data(UUID='%s', Model='%s', Value='%s')>" % (
                                self.dev_uuid, self.model, self.value)

class Device_Info(UserMixin, db.Model):
    __tablename__ = 'device_info'
    uuid = db.Column(db.String(64),unique=True, primary_key=True)
    name = db.Column(db.String(64))
    model = db.Column(db.String(64))
    online_status = db.Column(db.String(64))
    gw_uuid = db.Column(db.String(64))
    user_id = db.Column(db.String(64))
    associated = db.Column(db.String(64))
    target_energy_level = db.Column(db.Float(), default= 5)
    lower_bound = db.Column(db.Integer(), default = 10)
    start_time = db.Column(db.Integer(),default = 7)
    end_time = db.Column(db.Integer(),default = 18)
    notify = db.Column(db.String(64), default ="ON")
    
    @classmethod
    def get_by_userid(cls, userid):
        devices = Device_Info.query.filter_by(user_id=userid)
        return devices

    @classmethod
    def get_by_id(cls, id):
        device= Device_Info.query.get(id)
        return device

    def __repr__(self):
        return "<Device Info(UUID='%s', Name='%s', Model='%s' ,Goal='%s;, Target_energy_level='%s', Lower_bound='%s', Statr_time='%s', End_time='%s', Notify='%s' )>" % (
                                self.uuid, self.name, self.model,self.goal , self.target_energy_level, self.lower_bound, self.start_time, self.end_time, self.notify)

class User_Mgmt(UserMixin, db.Model):
    __tablename__ = 'user_mgmt'
    user_id = db.Column(db.String(64), unique=True, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64))
    activated = db.Column(db.String(64))
    notify_all = db.Column(db.String(64), default = "ON")
    
    @classmethod
    def get_by_id(cls, userid):
        user= User_Mgmt.query.get(id)
        return user

    def __repr__(self):
        return "<User Mgmt(UUID='%s', Name='%s', Email='%s', Notify_all='%s')>" % (
                                self.user_id, self.username, self.email, self.notify_all)

class Rules(UserMixin, db.Model):
    __tablename__ = 'rules'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(64))
    dev_uuid = db.Column(db.String(64), index=True)
    rule_info = db.Column(db.Text)

    def __repr__(self):
        return "<Rules Info(ID='%s', Name='%s', Info='%s')>" % (
                                self.id, self.name, self.rule_info)

class Notifications(UserMixin, db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.String(64))
    rule_id = db.Column(db.Integer)
    published = db.Column(db.Boolean)
    scheduled_time = db.Column(db.DateTime)
    content = db.Column(db.Text)

    def __repr__(self):
        return "<Notifications(ID='%s', Rule='%s', Content='%s')>" % (
                                self.id, self.rule_id, self.content)

class Posts(UserMixin, db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.String(64))
    rule_id = db.Column(db.Integer)
    published = db.Column(db.Boolean)
    scheduled_time = db.Column(db.DateTime)
    content = db.Column(db.Text)

    def __repr__(self):
        return "<Posts(ID='%s', Rule='%s', Content='%s')>" % (
                                self.id, self.rule_id, self.content)