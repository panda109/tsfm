# config.py
import os
basedir = os.path.abspath(os.path.dirname(__file__))
#UPLOADPATH = os.getcwd() + '\\static\\_upload\\images\\'
#P_IMAGEPATH = os.getcwd() + '\\static\\product\\images\\'
#S_IMAGEPATH = os.getcwd() + '\\static\\story\\images\\'

#UPLOADPATH = os.getcwd() + '/static/_upload/images/'
#P_IMAGEPATH = os.getcwd() + '/static/product/images/'
#S_IMAGEPATH = os.getcwd() + '/static/story/images/'

#IPPORT = 'bytaiwan.me'
IPPORT = '192.168.8.155:5000'
#IPPORT = '192.168.0.18:5000'
#IPPORT = '29fa258b.ngrok.io'
mailpassword=''

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '!QIOD*Lioisfhishiwiwe98ew9233'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SERVER_NAME = IPPORT
    SESSION_COOKIE_NAME = IPPORT
    SESSION_COOKIE_DOMAIN = IPPORT
        
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:1q2w3e4r@192.168.7.85:5432/test"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': ProductionConfig
}
