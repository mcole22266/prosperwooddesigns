# routes.py
# Michael Cole
#
# Location of all app routing
# ---------------------------

from flask import jsonify


class Routes:
    '''
    Routes object initializes a Flask app object in order to define all
    available routes

    Use:
        routes = Routes()
        routes.init(app)
    '''

    def init_app(self, app):
        '''
        Initializes a Flask app object with all available routes
        '''

        @app.route('/hello', methods=['GET'])
        def hello():
            return jsonify('Hello world')
