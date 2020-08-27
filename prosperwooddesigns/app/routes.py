# routes.py
# Michael Cole
#
# Location of all app routing
# ---------------------------

from flask import redirect, render_template, request, url_for

from flask_login import login_required, login_user, logout_user

from .extensions import DbConnector, Helper, Logger

logger = Logger()
dbConn = DbConnector()
helper = Helper()


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
            logger.log('Serving index page')
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
            logger.log('Serving designs page')
            return render_template('designs.html',
                                   title='Designs')

        @app.route('/requestform', methods=['GET', 'POST'])
        def requestform():
            '''
            Routes the user to the Request Form of the website
            '''
            from .forms import RequestForm

            requestform = RequestForm()
            if requestform.validate_on_submit():
                logger.log('Request form validated')

                email = request.form['email']
                phone = request.form['phone']
                name = request.form['name']
                contact_method = request.form['contact_method']
                description = request.form['description']
                how_hear = request.form['how_hear']

                dbConn.setRequest(
                    email, phone, name, contact_method, description, how_hear
                )

                logger.log('Redirecting to request form success page')
                return redirect(url_for('requestform_success'))

            logger.log('Serving request form page')
            return render_template('requestform.html',
                                   title='Request Form',
                                   requestform=requestform)

        @app.route('/requestform/success')
        def requestform_success():
            '''
            Routes the user to a confirmation page after submitting a
            request form
            '''
            logger.log('Serving request form success page')
            return render_template('requestform_success.html',
                                   title='Request Success')

        @app.route('/contact', methods=['GET', 'POST'])
        def contact():
            '''
            Routes the user to the Contact Form of the website
            '''
            from .forms import ContactForm

            contactform = ContactForm()
            if contactform.validate_on_submit():
                logger.log('Contact form validated')

                name = request.form['name']
                email = request.form['email']
                content = request.form['content']
                how_hear = request.form['how_hear']

                dbConn.setContact(email, name, content, how_hear)

                logger.log('Redirecting to contact form success page')
                return redirect(url_for('contact_success'))

            logger.log('Serving contact form page')
            return render_template('contact.html',
                                   title='Contact Form',
                                   contactform=contactform)

        @app.route('/contact/success')
        def contact_success():
            '''
            Routes the user to a confirmation page after submitting a
            contact form
            '''
            logger.log('Serving contact form success page')
            return render_template('contact_success.html',
                                   title='Contact Success')

        @app.route('/admin')
        @login_required
        def admin():
            '''
            Routes the user to the Admin Page of the website
            '''
            greeting = helper.getGreeting()
            requests = dbConn.getRequests(order_id=True)
            contacts = dbConn.getContacts(order_id=True)

            logger.log('Serving admin page')
            return render_template('admin.html',
                                   title='Admin',
                                   greeting=greeting,
                                   requests=requests,
                                   contacts=contacts)

        @app.route('/admin/log-in', methods=['GET', 'POST'])
        def admin_login():
            '''
            Routes the user to the Admin Log-In Page of the website
            '''
            from .forms import AdminLogInForm

            adminloginform = AdminLogInForm()
            if adminloginform.validate_on_submit():
                logger.log('Admin log-in form validated')

                username = request.form['username']
                # Currently handled by form -- TODO: Handle password auth
                # password = request.form['password']
                admin = dbConn.getAdmin(username=username)
                login_user(admin)
                next = request.args.get('next')

                logger.log('Redirecting to next or admin page')
                return redirect(next or url_for('admin'))

            logger.log('Serving admin log-in page')
            return render_template('admin-login.html',
                                   title='Admin - Log-In',
                                   adminloginform=adminloginform)

        @app.route('/admin/create', methods=['GET', 'POST'])
        def admin_create():
            '''
            Routes the user to the Admin Create Page of the website
            '''
            from .forms import AdminCreateForm

            admincreateform = AdminCreateForm()
            if admincreateform.validate_on_submit():
                logger.log('Admin create form validated')

                firstname = request.form['firstname']
                lastname = request.form['lastname']
                username = request.form['username']
                password = request.form['password']

                admin = dbConn.setAdmin(
                    username, password, firstname, lastname
                )

                login_user(admin)
                logger.log(f'{admin.username} logged in')

                logger.log('Redirecting to admin page')
                return redirect(url_for('admin'))

            logger.log('Serving admin create page')
            return render_template('admin-create.html',
                                   title='Admin - Create',
                                   admincreateform=admincreateform)

        @app.route('/admin/logout')
        @login_required
        def admin_logout():
            '''
            Logs a logged-in admin out and redirects to home-page
            '''

            logout_user()

            logger.log('Redirecting to index page')
            return redirect(url_for('index'))

        @app.route('/admin/request/update/<request_id>', methods=['POST'])
        @login_required
        def admin_request__update_requestid(request_id):
            '''
            Updated a request's status based on modal input
            '''
            new_status = request.form[f'request-{request_id}']

            if new_status == 'archive':
                dbConn.updateRequest(id=request_id, is_archived=True)
            else:
                dbConn.updateRequest(id=request_id, status=new_status)

            logger.log('Redirecting to admin page')
            return redirect(url_for('admin'))

        @app.route('/admin/request/delete/<request_id>', methods=['POST'])
        @login_required
        def admin_request_delete_requestid(request_id):
            '''
            Delete a request based on modal input
            '''
            dbConn.deleteRequest(request_id)

            logger.log('Redirecting to admin page')
            return redirect(url_for('admin'))

        @app.route('/admin/contact/update/<contact_id>', methods=['POST'])
        @login_required
        def admin_contact_contactid(contact_id):
            '''
            Updated a contact's status based on modal input
            '''
            new_status = request.form[f'contact-{contact_id}']

            if new_status == 'archive':
                dbConn.updateContact(id=contact_id, is_archived=True)
            else:
                dbConn.updateContact(id=contact_id, status=new_status)

            logger.log('Redirecting to admin page')
            return redirect(url_for('admin'))

        @app.route('/admin/contact/delete/<contact_id>', methods=['POST'])
        @login_required
        def admin_contact_delete_requestid(contact_id):
            '''
            Delete a contact based on modal input
            '''
            dbConn.deleteContact(contact_id)

            logger.log('Redirecting to admin page')
            return redirect(url_for('admin'))

        @app.route('/admin/data')
        @login_required
        def data():
            '''
            Routes the user to the Data Page of the website
            '''
            from .extensions import DbConnector

            dbConnector = DbConnector()

            admins = dbConnector.getAdmins()
            requests = dbConnector.getRequests()
            images = dbConnector.getImages()
            layouts = dbConnector.getLayouts()
            contacts = dbConnector.getContacts()

            logger.log('Serving admin data page')
            return render_template('data.html',
                                   title='Data',
                                   admins=admins,
                                   requests=requests,
                                   images=images,
                                   layouts=layouts,
                                   contacts=contacts)
