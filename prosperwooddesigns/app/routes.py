# routes.py
# Michael Cole
#
# Location of all app routing
# ---------------------------

from flask import redirect, render_template


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
            return render_template('index.html',
                                   title='Home')

        # CURRENTLY TABLED PENDING CLIENT'S THOUGHTS
        # @app.route('/about')
        # def about():
        #     '''
        #     Routes the user to the About Page of the website
        #     '''
        #     return render_template('about.html',
        #                            title='About')

        @app.route('/designs')
        def designs():
            '''
            Routes the user to the Designs Page of the website
            '''
            return render_template('designs.html',
                                   title='Designs')

        @app.route('/request')
        def request():
            '''
            Routes the user to the Request Form of the website
            '''
            from .forms import RequestForm
            requestform = RequestForm()
            if requestform.validate_on_submit():
                return redirect('request')
            return render_template('request.html',
                                   title='Request Form',
                                   requestform=requestform)

        @app.route('/contact')
        def contact():
            '''
            Routes the user to the Contact Form of the website
            '''
            from .forms import ContactForm
            contactform = ContactForm()
            if contactform.validate_on_submit():
                return redirect('contact')
            return render_template('contact.html',
                                   title='Contact Form',
                                   contactform=contactform)

        @app.route('/admin')
        def admin():
            '''
            Routes the user to the Admin Page of the website
            '''
            return render_template('admin.html',
                                   title='Admin')
