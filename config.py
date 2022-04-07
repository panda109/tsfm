# config.py
import os
from _ast import Pass
basedir = os.path.abspath(os.path.dirname(__file__))
#UPLOADPATH = os.getcwd() + '\\static\\_upload\\images\\'
#P_IMAGEPATH = os.getcwd() + '\\static\\product\\images\\'
#S_IMAGEPATH = os.getcwd() + '\\static\\story\\images\\'

#UPLOADPATH = os.getcwd() + '/static/_upload/images/'
#P_IMAGEPATH = os.getcwd() + '/static/product/images/'
#S_IMAGEPATH = os.getcwd() + '/static/story/images/'

#IPPORT = 'bytaiwan.me'
IPPORT = '192.168.7.62:5000'
#IPPORT = '192.168.0.18:5000'
#IPPORT = '29fa258b.ngrok.io'
mailpassword=''

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '!QIOD*Lioisfhishiwiwe98ew9233'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True
    BABEL_DEFAULT_LOCALE = 'zh_TW'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    #  這個部份就記得以你自己資料夾路徑來設置
    BABEL_TRANSLATION_DIRECTORIES = './app/templates'
    
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
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:1q2w3e4r@192.168.7.85:5432/TEST"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': TestingConfig
}
