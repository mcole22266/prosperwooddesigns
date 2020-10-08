# __init__.py
# Michael Cole
#
# App Factory Pattern implementation of create_app
# ------------------------------------------------

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

from app.extensions.DbConnector import DbConnector
from app.extensions.Logger import Logger
from app.extensions.MockData import MockData
from app.extensions.S3Connector import S3Connector
from app.extensions.Startup import Startup

from .models import db, loginManager
from .routes.Routes import Routes
from .routes.RoutesAdmin import RoutesAdmin

# Instantiate global variables
csrf = CSRFProtect()
flask_bcrypt = Bcrypt()
routes = Routes()
routesAdmin = RoutesAdmin()
logger = Logger()
s3Conn = S3Connector()
dbConn = DbConnector()
startup = Startup()
mockData = MockData()


def create_app():
    '''
    Creates a complete Flask app

    Returns:
        Flask App
    '''
    app = Flask(__name__, instance_relative_config=False,
                template_folder='./templates',  # define templates folder
                static_folder='./static')       # define static folder
    # config app with base variables
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
        routes.init_app(app)
        routesAdmin.init_app(app)

        logger.log('Initializing csrf protection')
        csrf.init_app(app)

        logger.log('Initializing encryption')
        flask_bcrypt.init_app(app)

        logger.log('Creating all tables in db')
        db.create_all()
        db.session.commit()

        logger.log('Initializing login manager')
        loginManager.init_app(app)
        # define where login protected routes should route user to log-in
        loginManager.login_view = 'admin_login'

        if app.config['GENERATE_FAKE_DATA']:
            # by default, fake data will only be generated
            # if in development and no data currently exists
            logger.log('Checking if fake data is present')
            if not mockData.hasData(db):
                logger.log('Generating fake data')
                if app.config['GENERATE_FAKE_DATA_ADMIN']:
                    mockData.loadAdmin(db)
                if app.config['GENERATE_FAKE_DATA_REQUEST']:
                    mockData.loadRequest(db)
                if app.config['GENERATE_FAKE_DATA_LAYOUT']:
                    mockData.loadLayout(db)
                if app.config['GENERATE_FAKE_DATA_QUESTION']:
                    mockData.loadQuestion(db)
                if app.config['GENERATE_FAKE_DATA_CONTACT']:
                    mockData.loadContact(db)
                if app.config['GENERATE_FAKE_DATA_PRODUCT']:
                    mockData.loadProduct(db)
                if app.config['GENERATE_FAKE_DATA_IMAGE']:
                    mockData.loadImage(db)
                if app.config['GENERATE_FAKE_DATA_VISITOR']:
                    mockData.loadVisitor(db)
            else:
                logger.log('Fake data already present')

        if app.config['DB_INIT_DATA']:
            # by default, database will be initialized with
            # default data
            logger.log('Checking if initial data is present')
            if not startup.hasData(db):
                logger.log('Loading initial data')
                startup.loadInitialData()
            else:
                logger.log('Initial data already present')

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
