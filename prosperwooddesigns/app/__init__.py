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
    app = Flask(__name__, instance_relative_config=False,
                template_folder='./templates',
                static_folder='./static')
    app.config.from_object('config.ConfigDev')

    with app.app_context():

        routes.init(app)

        return app
