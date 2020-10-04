# config.py
# Michael Cole
#
# Configuration file for Flask which will be
# consumed by the app object
# ------------------------------------------

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
    DB_TEST_ADMIN_USERNAME = environ['DB_TEST_ADMIN_USERNAME']
    DB_TEST_ADMIN_PASSWORD = environ['DB_TEST_ADMIN_PASSWORD']
    DB_TEST_ADMIN_FIRSTNAME = environ['DB_TEST_ADMIN_FIRSTNAME']
    DB_TEST_ADMIN_LASTNAME = environ['DB_TEST_ADMIN_LASTNAME']

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

    # Other Config
    ADMIN_FORM_SECRET_CODE = environ['ADMIN_FORM_SECRET_CODE']


class ConfigDev:
    '''
    Development Configuration
    '''

    # General Config
    DB_CREATE_ADMIN_USER = True         # creates dev admin user
    DB_INIT_DATA = True                 # creates initial data
    LOG_TO_STDOUT = True                # logs go to stdout
    LOG_TO_FILE = False                 # logs go to log files
    ADMIN_AUTO_LOGIN = True             # auto login as admin at index page


    # MockData Config
    GENERATE_FAKE_DATA = True           # generates mockdata upon startup
    # None of the below will generate if GENERATE_FAKE_DATA==False
    GENERATE_FAKE_DATA_ADMIN = True     # generates mock admin upon startup
    GENERATE_FAKE_DATA_REQUEST = True   # generates mock request upon startup
    GENERATE_FAKE_DATA_LAYOUT = True    # generates mock layout upon startup
    GENERATE_FAKE_DATA_QUESTION = True  # generates mock question upon startup
    GENERATE_FAKE_DATA_CONTACT = True   # generates mock contact upon startup
    GENERATE_FAKE_DATA_PRODUCT = False  # generates mock product upon startup
    GENERATE_FAKE_DATA_IMAGE = False    # generates mock image upon startup

    # SQLAlchemy Config
    SQLALCHEMY_ECHO = False             # SQLAlchemy verbose output

    # AWS Config
    AWS_DOWNLOAD_IMAGES = False         # download images from S3 bucket


class ConfigProd:
    '''
    Production Configuration
    '''

    # General Config
    DB_CREATE_ADMIN_USER = False        # creates dev admin user
    LOG_TO_STDOUT = False               # logs go to stdout
    LOG_TO_FILE = True                  # logs go to log files
    ADMIN_AUTO_LOGIN = False            # auto login as admin at index page

    # MockData Config
    GENERATE_FAKE_DATA = False          # generates mockdata upon startup
    # None of the below will generate if GENERATE_FAKE_DATA==False
    GENERATE_FAKE_DATA_ADMIN = False    # generates mock admin upon startup
    GENERATE_FAKE_DATA_REQUEST = False  # generates mock request upon startup
    GENERATE_FAKE_DATA_LAYOUT = False   # generates mock layout upon startup
    # generates mock question upon startup
    GENERATE_FAKE_DATA_QUESTION = False
    GENERATE_FAKE_DATA_CONTACT = False  # generates mock contact upon startup
    GENERATE_FAKE_DATA_PRODUCT = False  # generates mock product upon startup
    GENERATE_FAKE_DATA_IMAGE = False    # generates mock image upon startup

    # SQLAlchemy Config
    SQLALCHEMY_ECHO = False             # SQLAlchemy verbose output

    # AWS Config
    AWS_DOWNLOAD_IMAGES = True          # download images from S3 bucket
