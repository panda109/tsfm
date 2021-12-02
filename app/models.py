# app/models.py

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
    
##ass User(UserMixin, db.Model):
##  __tablename__ = 'users'
##  id = db.Column(db.Integer, primary_key=True)
##  username = db.Column(db.String(64), unique=True, index=True)
##  email = db.Column(db.String(64), unique=True, index=True)
##
##  @classmethod
##  def get_role(cls, orle_id):
##      role = Role.query.filter_by(id=orle_id)
##      return role
##
##  @classmethod
##  def get_all(cls):
##      users = User.query.all()
##      return users
##
##  @property
##  def password(self):
##      raise AttributeError('password is not a readable attribute')
##
##  @password.setter
##  def password(self, password):
##      self.password_hash = generate_password_hash(password, method="pbkdf2:sha1")
##
##  def verify_password(self, password):
##      return check_password_hash(self.password_hash, password)
##
##  def generate_confirmation_token(self, expiration=3600):
##      s = Serializer(current_app.config['SECRET_KEY'], expiration)
##      return s.dumps({'confirm': self.id}).decode('utf-8')
##
##  def confirm(self, token):
##      s = Serializer(current_app.config['SECRET_KEY'])
##      try:
##          data = s.loads(token.encode('utf-8'))
##      except:
##          return False
##
##      if data.get('confirm') != self.id:
##          return False
##
##      self.confirmed = True
##      db.session.add(self)
##      return True
##
##  def generate_reset_token(self, expiration=3600):
##      s = Serializer(current_app.config['SECRET_KEY'], expiration)
##      return s.dumps({'reset': self.id}).decode('utf-8')
##
##  @staticmethod
##  def reset_password(token, new_password):
##      s = Serializer(current_app.config['SECRET_KEY'])
##      try:
##          data = s.loads(token.encode('utf-8'))
##      except:
##          return False
##
##      user = User.query.get(data.get('reset'))
##      if user is None:
##          return False
##
##      user.password = new_password
##      db.session.add(user)
##      return True
##
##  def generate_email_change_token(self, new_email, expiration=3600):
##      s = Serializer(current_app.config['SECRET_KEY'], expiration)
##      return s.dumps(
##          {'change_email': self.id, 'new_email': new_email}).decode('utf-8')
##
##  def change_email(self, token):
##      s = Serializer(current_app.config['SECRET_KEY'])
##      try:
##          data = s.loads(token.encode('utf-8'))
##      except:
##          return False
##
##      if data.get('change_email') != self.id:
##          return False
##
##      new_email = data.get('new_email')
##      if new_email is None:
##          return False
##
##      if self.query.filter_by(email=new_email).first() is not None:
##          return False
##
##      self.email = new_email
##      db.session.add(self)
##      return True
##
##  def __repr__(self):
##      return '<User %r>' % self.username

class Device_Data(UserMixin, db.Model):
    __tablename__ = 'device_data'
    id = db.Column(db.Integer, primary_key=True)
    dev_uuid = db.Column(db.String(64), unique=True, index=True)
    scope = db.Column(db.String(64))
    model = db.Column(db.String(64))
    value = db.Column(db.Integer)
    generated_time = db.Column(db.DateTime)
    uploaded_time = db.Column(db.DateTime)

    def __repr__(self):
        return "<Device Data(UUID='%s', Model='%s', Value='%s')>" % (
                                self.dev_uuid, self.model, self.value)

class Device_Info(UserMixin, db.Model):
    __tablename__ = 'device_info'
    uuid = db.Column(db.String(64),unique=True, primary_key=True)
    name = db.Column(db.String(64))
    model = db.Column(db.String(64))
    online_status = db.Column(db.Integer)
    gw_uuid = db.Column(db.String(64))
    user_id = db.Column(db.String(64))
    associated = db.Column(db.Boolean)
    notify = db.Column(db.String(64), default ="ON")

    def __repr__(self):
        return "<Device Info(UUID='%s', Name='%s', Model='%s')>" % (
                                self.uuid, self.name, self.model)

class User_Mgmt(UserMixin, db.Model):
    __tablename__ = 'user_mgmt'
    user_id = db.Column(db.String(64), unique=True, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64))
    activated = db.Column(db.Boolean)
    activated_time = db.Column(db.DateTime)
    expired_time = db.Column(db.DateTime)
    notify_all = db.Column(db.String(64), default = "ON")

    def __repr__(self):
        return "<User Mgmt(UUID='%s', Name='%s', Email='%s')>" % (
                                self.user_id, self.name, self.email)

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