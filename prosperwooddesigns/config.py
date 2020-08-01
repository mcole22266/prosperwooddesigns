# config.py
# Michael Cole
#
# OOP Configuration file for Flask
# --------------------------------

from os import environ, urandom


class ConfigDev:
    '''
    Development Configuration
    '''

    # Flask App Settings
    FLASK_ENV = environ['FLASK_ENV']
    FLASK_APP = environ['FLASK_APP']
    FLASK_RUN_HOST = environ['FLASK_RUN_HOST']
    SECRET_KEY = urandom(16)

    # AWS Settings
    AWS_ACCESS_KEY_ID = environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = environ['AWS_SECRET_ACCESS_KEY']
    AWS_PROJECT_BUCKET = environ['AWS_PROJECT_BUCKET']
    AWS_PROJECT_BUCKET_IMAGE_DIR = environ['AWS_PROJECT_BUCKET_IMAGE_DIR']
    AWS_LOCAL_IMAGE_PATH = environ['AWS_LOCAL_IMAGE_PATH']
