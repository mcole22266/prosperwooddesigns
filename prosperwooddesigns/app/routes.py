# routes.py
# Michael Cole
#
# Defines all app's routing logic
# --------------------------------

from flask import redirect, render_template, request, url_for

from app.extensions.DbConnector import DbConnector
from app.extensions.Helper import Helper
from app.extensions.Logger import Logger
from flask_login import login_required, login_user, logout_user

# instantiate variables
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

    def init_app(self, app):
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

                # Get form data
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

        @app.route('/questionform', methods=['GET', 'POST'])
        def questionform():
            '''
            Routes the user to the Question Form of the website
            '''
            from .forms import QuestionForm

            questionform = QuestionForm()
            if questionform.validate_on_submit():
                logger.log('Question form validated')

                # get form data
                name = request.form['name']
                email = request.form['email']
                content = request.form['content']
                how_hear = request.form['how_hear']

                dbConn.setQuestion(email, name, content, how_hear)

                logger.log('Redirecting to question form success page')
                return redirect(url_for('questionform_success'))

            logger.log('Serving question form page')
            return render_template('questionform.html',
                                   title='Question Form',
                                   questionform=questionform)

        @app.route('/questionform/success')
        def questionform_success():
            '''
            Routes the user to a confirmation page after submitting a
            question form
            '''
            logger.log('Serving question form success page')
            return render_template('questionform_success.html',
                                   title='Question Success')

        @app.route('/admin')
        @login_required
        def admin():
            '''
            Routes the user to the Admin Page of the website
            '''
            # get data to be used in page
            greeting = helper.getGreeting()
            requests = dbConn.getRequests(order_id=True)
            questions = dbConn.getQuestions(order_id=True)

            logger.log('Serving admin page')
            return render_template('admin.html',
                                   title='Admin',
                                   greeting=greeting,
                                   requests=requests,
                                   questions=questions)

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
                # Password confirmation is handled client-side.
                # If implementation changes to server-side, uncomment
                # the below line and validate password
                # password = request.form['password']

                # Log user in after form has submitted
                admin = dbConn.getAdmin(username=username)
                login_user(admin)
                next = request.args.get('next')  # get next-page location

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

                # get form data
                firstname = request.form['firstname']
                lastname = request.form['lastname']
                username = request.form['username']
                password = request.form['password']

                # Create Admin
                admin = dbConn.setAdmin(
                    username, password, firstname, lastname
                )

                # go ahead and log user in
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

            # Log user out of the app
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

            # If status is "archive" then is_archived will be set to True
            # while status will be left as-is
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

        @app.route('/admin/question/update/<question_id>', methods=['POST'])
        @login_required
        def admin_question_questionid(question_id):
            '''
            Updated a Question's status based on modal input
            '''
            new_status = request.form[f'question-{question_id}']

            # If status is "archive" then is_archived will be set to True
            # while status will be left as-is
            if new_status == 'archive':
                dbConn.updateQuestion(id=question_id, is_archived=True)
            else:
                dbConn.updateQuestion(id=question_id, status=new_status)

            logger.log('Redirecting to admin page')
            return redirect(url_for('admin'))

        @app.route('/admin/question/delete/<question_id>', methods=['POST'])
        @login_required
        def admin_question_delete_question_id(question_id):
            '''
            Delete a question based on modal input
            '''
            dbConn.deleteQuestion(question_id)

            logger.log('Redirecting to admin page')
            return redirect(url_for('admin'))

        @app.route('/admin/data')
        @login_required
        def data():
            '''
            Routes the user to the Data Page of the website
            '''
            from app.extensions.DbConnector import DbConnector

            dbConnector = DbConnector()

            # get data for front-end presentation
            admins = dbConnector.getAdmins()
            requests = dbConnector.getRequests()
            images = dbConnector.getImages()
            layouts = dbConnector.getLayouts()
            questions = dbConnector.getQuestions()

            logger.log('Serving admin data page')
            return render_template('data.html',
                                   title='Data',
                                   admins=admins,
                                   requests=requests,
                                   images=images,
                                   layouts=layouts,
                                   questions=questions)
