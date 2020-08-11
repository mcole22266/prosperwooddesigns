# config.py
# Michael Cole
#
# OOP Configuration file for Flask
# --------------------------------

from os import environ, urandom


class ConfigBase:
    '''
    Base Configuration
    '''

    # Flask App Config
    FLASK_ENV = environ['FLASK_ENV']
    FLASK_APP = environ['FLASK_APP']
    FLASK_RUN_HOST = environ['FLASK_RUN_HOST']
    SECRET_KEY = urandom(16)

    # Postgres Config
    POSTGRES_USER = environ['POSTGRES_USER']
    POSTGRES_PASSWORD = environ['POSTGRES_PASSWORD']
    POSTGRES_DB = environ['POSTGRES_DB']

    # Flask SQLAlchemy Config
    SQLALCHEMY_TRACK_MODIFICATIONS = environ['SQLALCHEMY_TRACK_MODIFICATIONS']
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
        f'@db:5432/{POSTGRES_DB}'
        )

    # AWS Config
    AWS_ACCESS_KEY_ID = environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = environ['AWS_SECRET_ACCESS_KEY']
    AWS_PROJECT_BUCKET = environ['AWS_PROJECT_BUCKET']
    AWS_PROJECT_BUCKET_IMAGE_DIR = environ['AWS_PROJECT_BUCKET_IMAGE_DIR']
    AWS_LOCAL_IMAGE_PATH = environ['AWS_LOCAL_IMAGE_PATH']


class ConfigDev:
    '''
    Development Configuration
    '''

    # SQLAlchemy Config
    SQLALCHEMY_ECHO = False

    # AWS Config
    AWS_DOWNLOAD_IMAGES = False


class ConfigProd:
    '''
    Production Configuration
    '''

    # SQLAlchemy Config
    SQLALCHEMY_ECHO = False

    # AWS Config
    AWS_DOWNLOAD_IMAGES = True
