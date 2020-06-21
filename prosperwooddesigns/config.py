# config.py
# Michael Cole
#
# OOP Configuration file for Flask
# --------------------------------
from os import environ


class ConfigDev:
    '''
    Development Configuration
    '''
    FLASK_ENV = environ['FLASK_ENV']
    FLASK_APP = environ['FLASK_APP']
    FLASK_RUN_HOST = environ['FLASK_RUN_HOST']
