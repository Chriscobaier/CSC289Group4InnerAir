from decouple import config

DB_NAME = 'inner-air-dev.db'


class Config(object):
    SECRET_KEY = config('SECRET_KEY', default='`5J<-lgHQaae_|LR*h)0%}`#k?sW@IK],P-9,A/}d`Ly&GwruSUh#omM]AdXwNP')
    SECURITY_PASSWORD_SALT = config('SECURITY_PASSWORD_SALT', default='a56ad0d9ed8e7ed487f2939f1d161e27')

    """
        mail settings
    """
    MAIL_DEFAULT_SENDER = 'c626521@gmail.com'
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
