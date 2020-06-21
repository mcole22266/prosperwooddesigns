# routes.py
# Michael Cole
#
# Location of all app routing
# ---------------------------


class Routes:
    '''
    Routes object initializes a Flask app object in order to define all
    available routes

    Use:
        routes = Routes()
        routes.init(app)
    '''

    def init(self, app):
        '''
        Initializes a Flask app object with all available routes
        '''

        @app.route('/')
        def index():
            return 'Hello World'
