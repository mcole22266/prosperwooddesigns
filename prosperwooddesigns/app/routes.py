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

        @app.route('/about')
        def about():
            '''
            Routes the user to the About Page of the website
            '''
            return render_template('about.html',
                                   title='About')

        @app.route('/designs')
        def designs():
            '''
            Routes the user to the Designs Page of the website
            '''
            return render_template('designs.html',
                                   title='Designs')

        @app.route('/order')
        def order():
            '''
            Routes the user to the Order Form of the website
            '''
            from .forms import OrderForm
            orderform = OrderForm()
            if orderform.validate_on_submit():
                return redirect('order')
            return render_template('order.html',
                                   title='Order Form',
                                   orderform=orderform)

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
