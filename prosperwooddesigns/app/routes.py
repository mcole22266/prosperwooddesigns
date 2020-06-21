class Routes:

    def init(self, app):

        @app.route('/')
        def index():
            return 'Hello World'