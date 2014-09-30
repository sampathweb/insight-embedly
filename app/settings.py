import os


class Config(object):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ProdConfig(Config):
    APP_SERVER = 'PROD'
    SECRET_KEY = 'prod - tis is secret?'


class DevConfig(Config):
    APP_SERVER = 'DEV'
    SECRET_KEY = 'dev - tis is secret?'
