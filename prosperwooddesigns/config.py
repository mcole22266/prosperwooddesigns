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
