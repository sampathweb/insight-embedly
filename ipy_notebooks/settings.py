import os


class Config(object):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ProdConfig(Config):
    APP_SERVER = 'PROD'
    EVENTS_BUCKET = ''
    SECRET_KEY = 'prod - tis is secret?'
    # SQL Alchemy settings
    SQLALCHEMY_DATABASE_URI = 'postgresql://dbadmin:2Insight!@insight-ramesh-dw.cniqeoxrupxt.us-west-2.redshift.amazonaws.com:5439/dev'


class DevConfig(Config):
    APP_SERVER = 'DEV'
    EVENTS_BUCKET = ''
    SECRET_KEY = 'dev - tis is secret?'
    # SQL Alchemy settings
    SQLALCHEMY_DATABASE_URI = 'postgresql://dbadmin:2Insight!@insight-ramesh-dw.cniqeoxrupxt.us-west-2.redshift.amazonaws.com:5439/dev'
