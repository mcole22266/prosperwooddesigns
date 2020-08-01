# __init__.py
# Michael Cole
#
# App Factory Pattern implementation of create_app
# ------------------------------------------------

from flask import Flask

from flask_wtf.csrf import CSRFProtect

from .routes import Routes
from .extensions import Logger

routes = Routes()
csrf = CSRFProtect()
logger = Logger()


def create_app():
    '''
    Creates a complete Flask app

    Returns:
        Flask App
    '''
    logger.log('Creating app')
    app = Flask(__name__, instance_relative_config=False,
                template_folder='./templates',
                static_folder='./static')
    app.config.from_object('config.ConfigDev')

    with app.app_context():

        logger.log('Importing routes')
        routes.init(app)
        logger.log('Initializing csrf protection')
        csrf.init_app(app)

        return app
