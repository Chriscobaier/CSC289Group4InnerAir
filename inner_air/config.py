from decouple import config

DB_NAME = config('DB_NAME')


class Config(object):
    """
        base config.
    """
    SECRET_KEY = config('SECRET_KEY')
    SECURITY_PASSWORD_SALT = config('SECURITY_PASSWORD_SALT')
    DEBUG = False
    DEBUG_TB_ENABLED = False

    """
        mail settings.
    """
    MAIL_DEFAULT_SENDER = config('APP_MAIL_DEFAULT_SENDER')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = config('APP_MAIL_USERNAME')
    MAIL_PASSWORD = config('APP_MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_ENABLED = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    DEBUG = False
    DEBUG_TB_ENABLED = False
