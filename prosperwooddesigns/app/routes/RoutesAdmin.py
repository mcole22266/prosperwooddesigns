# RoutesAdmin.py
# Michael Cole
#
# Defines all app's Admin routing logic
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


class RoutesAdmin:
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

        @app.route('/admin')
        @login_required
        def admin():
            '''
            Routes the user to the Admin Page of the website
            '''
            logger.log('Serving admin page')
            return render_template('admin/dashboard.html',
                                   title='Admin: Dashboard')

        @app.route('/admin/log-in', methods=['GET', 'POST'])
        def admin_login():
            '''
            Routes the user to the Admin Log-In Page of the website
            '''
            from app.forms import AdminLogInForm
            from flask_login import current_user

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
                logger.log(f'Logging in {current_user}')
                login_user(admin)
                logger.log(f'Logged in {current_user}')
                next = request.args.get('next')  # get next-page location

                logger.log('Redirecting to next or admin page')
                return redirect(next or url_for('admin'))

            logger.log('Serving admin log-in page')
            return render_template('admin/admin-login.html',
                                   title='Admin - Log-In',
                                   adminloginform=adminloginform)

        @app.route('/admin/create', methods=['GET', 'POST'])
        def admin_create():
            '''
            Routes the user to the Admin Create Page of the website
            '''
            from app.forms import AdminCreateForm

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
            return render_template('admin/admin-create.html',
                                   title='Admin - Create',
                                   admincreateform=admincreateform)

        @app.route('/admin/logout')
        @login_required
        def admin_logout():
            '''
            Logs a logged-in admin out and redirects to home-page
            '''
            from flask_login import current_user

            # Log user out of the app
            logger.log(f'Logging out {current_user}')
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
            return redirect(url_for('admin_project_management_requests'))

        @app.route('/admin/request/delete/<request_id>', methods=['POST'])
        @login_required
        def admin_request_delete_requestid(request_id):
            '''
            Delete a request based on modal input
            '''
            dbConn.deleteRequest(request_id)

            logger.log('Redirecting to admin page')
            return redirect(url_for('admin_project_management_requests'))

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
            return redirect(url_for('admin_project_management_questions'))

        @app.route('/admin/question/delete/<question_id>', methods=['POST'])
        @login_required
        def admin_question_delete_question_id(question_id):
            '''
            Delete a question based on modal input
            '''
            dbConn.deleteQuestion(question_id)

            logger.log('Redirecting to admin page')
            return redirect(url_for('admin_project_management_questions'))

        @app.route('/admin/data')
        @login_required
        def data():
            '''
            Routes the user to the Data Page of the website
            '''
            from app.extensions.DbConnector import DbConnector

            dbConn = DbConnector()

            # get data for front-end presentation
            admins = dbConn.getAdmins()
            requests = dbConn.getRequests()
            images = dbConn.getImages()
            layouts = dbConn.getLayouts()
            questions = dbConn.getQuestions()
            contacts = dbConn.getContacts()
            products = dbConn.getProducts()

            logger.log('Serving admin data page')
            return render_template('admin/data.html',
                                   title='Admin: Data',
                                   admins=admins,
                                   requests=requests,
                                   images=images,
                                   layouts=layouts,
                                   questions=questions,
                                   contacts=contacts,
                                   products=products)

        @app.route('/admin/project-management/requests')
        @login_required
        def admin_project_management_requests():
            '''
            Routes the user to the Requests Management page of the website
            '''
            # get data to be used in page
            requests = dbConn.getRequests(order_id=True)

            logger.log('Serving Project Management page')
            return render_template('admin/project-management-requests.html',
                                   title='Admin: Project Management',
                                   requests=requests)

        @app.route('/admin/project-management/questions')
        @login_required
        def admin_project_management_questions():
            '''
            Routes the user to the Questions Management page of the website
            '''
            # get data to be used in page
            questions = dbConn.getQuestions(order_id=True)

            logger.log('Serving Project Management page')
            return render_template('admin/project-management-questions.html',
                                   title='Admin: Project Management',
                                   questions=questions)

        @app.route('/admin/project-management/contacts')
        @login_required
        def admin_project_management_contacts():
            '''
            Routes the user to the Contacts Management page of the website
            '''
            # get data to be used in page
            contacts = dbConn.getContacts(order_id=True)

            logger.log('Serving Project Management page')
            return render_template('admin/project-management-contacts.html',
                                   title='Admin: Project Management',
                                   contacts=contacts)

        @app.route('/admin/product-management')
        @login_required
        def admin_product_management():
            '''
            Routes the user to the Admin Product Management page of the website
            '''
            # get data to be used in page
            productsImages = dbConn.getJoined_ProductImages()
            featuredProductsImages = dbConn.getJoined_ProductImages(
                featuredProducts=True)
            productsFeaturedImages = dbConn.getJoined_ProductImages(
                featuredImages=True)

            logger.log('Serving Product Management Page')
            return render_template(
                'admin/product-management.html',
                title='Admin: Product Management',
                productsImages=productsImages,
                featuredProductsImages=featuredProductsImages,
                productsFeaturedImages=productsFeaturedImages
                )

        @app.route('/admin/product-management/update/<product_id>',
                   methods=['POST'])
        @login_required
        def admin_product_productid(product_id):
            '''
            Updated a Product's information based on modal input
            '''
            # get values from form
            product_name = request.form[f'productName-{product_id}']
            product_description = request.form[
                f'productDescription-{product_id}'
                ]
            # try/except on is_featured_product because if toggle
            # is off then no value will be posted
            try:
                is_featured_product = request.form[
                    f'is_featured_product-{product_id}'
                    ]
                is_featured_product = True
            except KeyError:
                is_featured_product = False

            # download image file if there is one
            if request.files['imageFile']:
                imageFile = request.files['imageFile']
                imageFile.save(f'/prosperwooddesigns/{imageFile.filename}')

            # update product
            dbConn.updateProduct(
                id=product_id, name=product_name,
                description=product_description,
                is_featured_product=is_featured_product)

            logger.log('Redirecting to admin page')
            return redirect(url_for('admin_product_management'))

        @app.route('/admin/product-management/delete/<product_id>',
                   methods=['POST'])
        @login_required
        def admin_product_delete_productid(product_id):
            '''
            Delete a Product based on modal input
            '''
            # Delete the product
            dbConn.deleteProduct(id=product_id)

            logger.log('Redirecting to admin page')
            return redirect(url_for('admin_product_management'))
