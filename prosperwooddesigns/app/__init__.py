# __init__.py
# Michael Cole
#
# App Factory Pattern implementation of create_app
# ------------------------------------------------

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from .routes import Routes
from .models import db
from .extensions import Logger, S3Connecter

csrf = CSRFProtect()
routes = Routes()
logger = Logger()
s3Conn = S3Connecter()


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
    # configure app with base vars
    app.config.from_object('config.ConfigBase')

    if app.config['FLASK_ENV'] == 'development':
        # config app with dev config
        app.config.from_object('config.ConfigDev')
    elif app.config['FLASK_ENV'] == 'production':
        # config app with prod config
        app.config.from_object('config.ConfigProd')

    if app.config['AWS_DOWNLOAD_IMAGES']:
        # by default, will only download images on startup
        # if in production
        logger.log('Importing remote image files from S3')
        s3Conn.downloadImages()

    logger.log('Initializing DB')
    db.init_app(app)

    with app.app_context():

        logger.log('Importing routes')
        routes.init(app)
        logger.log('Initializing csrf protection')
        csrf.init_app(app)
        logger.log('Creating all tables in db')
        db.create_all()
        db.session.commit()

        logger.log('App created')
        return app
