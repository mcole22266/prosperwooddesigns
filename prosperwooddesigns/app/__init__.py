from flask import Flask

from .routes import Routes

routes = Routes()

def create_app():
    app = Flask(__name__, instance_relative_config=False)

    with app.app_context():

        routes.init(app)

        return app
