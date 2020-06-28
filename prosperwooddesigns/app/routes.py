# routes.py
# Michael Cole
#
# Location of all app routing
# ---------------------------

from flask import render_template


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
            '''
            Routes the user to the Landing Page of the website
            '''
            return render_template('index.html')

        @app.route('/about')
        def about():
            '''
            Routes the user to the About Page of the website
            '''
            return 'About Page'

        @app.route('/designs')
        def designs():
            '''
            Routes the user to the Designs Page of the website
            '''
            return 'Designs Page'

        @app.route('/order')
        def order():
            '''
            Routes the user to the Order Form of the website
            '''
            return 'Order Form'

        @app.route('/admin')
        def admin():
            '''
            Routes the user to the Admin Page of the website
            '''
            return 'Admin Page'
