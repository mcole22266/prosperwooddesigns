# __init__.py
# Michael Cole
#
# App Factory Pattern implementation of create_app
# ------------------------------------------------

from flask import Flask

from .routes import Routes

routes = Routes()


def create_app():
    '''
    Creates a complete Flask app

    Returns:
        Flask App
    '''
    app = Flask(__name__, instance_relative_config=False)

    # configure app with base vars
    app.config.from_object('config.ConfigBase')

    if app.config['FLASK_ENV'] == 'development':
        # config app with dev config
        app.config.from_object('config.ConfigDev')
    elif app.config['FLASK_ENV'] == 'production':
        # config app with prod config
        app.config.from_object('config.ConfigProd')

    with app.app_context():

        routes.init_app(app)

        return app
