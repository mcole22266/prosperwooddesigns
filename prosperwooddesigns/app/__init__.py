# __init__.py
# Michael Cole
#
# App Factory Pattern implementation of create_app
# ------------------------------------------------

from flask import Flask

from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

from .extensions import DbConnector, Logger, MockData, S3Connecter
from .models import db, loginManager
from .routes import Routes

csrf = CSRFProtect()
flask_bcrypt = Bcrypt()
routes = Routes()
logger = Logger()
s3Conn = S3Connecter()
dbConn = DbConnector()
mockData = MockData()


def create_app():
    '''
    Creates a complete Flask app

    Returns:
        Flask App
    '''
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

    # logger.log('Initializing DB')
    db.init_app(app)

    with app.app_context():
        logger.log('Creating App')

        if app.config['AWS_DOWNLOAD_IMAGES']:
            # by default, will only download images on startup
            # if in production
            s3Conn.downloadImages()

        logger.log('Importing routes')
        routes.init(app)
        logger.log('Initializing csrf protection')
        csrf.init_app(app)
        logger.log('Initializing encryption')
        flask_bcrypt.init_app(app)
        logger.log('Creating all tables in db')
        db.create_all()
        db.session.commit()
        logger.log('Initializing login manager')
        loginManager.init_app(app)
        loginManager.login_view = 'admin_login'

        if app.config['GENERATE_FAKE_DATA']:
            # by default, fake data will only be generated
            # if in development and no data currently exists
            logger.log('Checking if fake data is present')
            if not mockData.hasData(db):
                logger.log('Generating fake data')
                mockData.loadAdmin(db)
                mockData.loadRequest(db)
                mockData.loadImage(db)
                mockData.loadLayout(db)
                mockData.loadContact(db)
            else:
                logger.log('Fake data already present')

        if app.config['DB_CREATE_ADMIN_USER']:
            # by default, will create generic admin user
            # if in development mode
            username = app.config['DB_TEST_ADMIN_USERNAME']
            password = app.config['DB_TEST_ADMIN_PASSWORD']
            firstname = app.config['DB_TEST_ADMIN_FIRSTNAME']
            lastname = app.config['DB_TEST_ADMIN_LASTNAME']
            logger.log('Checking if generic admin user already exists')
            if dbConn.getAdmin(username=username):
                logger.log('Generic admin user exists')
            else:
                logger.log('Creating generic admin user')
                dbConn.setAdmin(username, password, firstname, lastname)

        logger.log('App created')
        return app
