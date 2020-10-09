# RoutesAdmin.py
# Michael Cole
#
# Defines all app's Admin routing logic
# --------------------------------

from datetime import datetime

from app.extensions.DbConnector import DbConnector
from app.extensions.Helper import Helper
from app.extensions.Logger import Logger
from flask import redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.exceptions import BadRequestKeyError

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

            # get Unique Visitors info
            uniqueVisitors = dbConn.getVisitorsPerMonth(exclude_admins=True)

            # Get total visitor count
            totalUniqueVisitors = 0
            for label, data in uniqueVisitors:
                # increments total unique visitors
                totalUniqueVisitors += data

            #  Get average visitors per month
            averageVisitorsPerMonth = round(
                totalUniqueVisitors / len(uniqueVisitors),
                2)

            # Get Data for the Dashboard Graph
            # only show a maximum of 12 months on the Dashboard Graph
            if len(uniqueVisitors) > 12:
                uniqueVisitors = uniqueVisitors[-12:]
            uniqueVisitors_labels = []
            uniqueVisitors_data = []
            for label, data in uniqueVisitors:
                uniqueVisitors_labels.append(label)
                uniqueVisitors_data.append(data)

            # get data for the Dashboard Pie Chart
            marketingStats = dbConn.getMarketingStats()
            marketingStats_labels = []
            marketingStats_data = []
            for label, data in marketingStats:
                marketingStats_labels.append(label)
                marketingStats_data.append(data)

            # get total number of products
            products = dbConn.getProducts()
            numProducts = len(products)

            # get number of completed requests
            completedRequests = dbConn.getRequests(complete=True)
            numCompletedRequests = len(completedRequests)

            # get unread messages
            unreadRequests = dbConn.getRequests(unread=True)
            unreadQuestions = dbConn.getQuestions(unread=True)

            logger.log('Serving admin page')
            return render_template(
                'admin/dashboard.html',
                title='Admin: Dashboard',
                totalUniqueVisitors=totalUniqueVisitors,
                averageVisitorsPerMonth=averageVisitorsPerMonth,
                numProducts=numProducts,
                numCompletedRequests=numCompletedRequests,
                uniqueVisitors_labels=uniqueVisitors_labels,
                uniqueVisitors_data=uniqueVisitors_data,
                marketingStats_labels=marketingStats_labels,
                marketingStats_data=marketingStats_data,
                unreadRequests=unreadRequests,
                unreadQuestions=unreadQuestions
                )

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
                # set Visitor.is_admin to True
                dbConn.setVisitor(request.remote_addr, is_admin=True)
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
                # set Visitor.is_admin to True
                dbConn.setVisitor(request.remote_addr, is_admin=True)

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

        @app.route('/admin/contact/delete/<contact_id>', methods=['POST'])
        @login_required
        def admin_contact_delete_contact_id(contact_id):
            '''
            Delete a contact based on modal input
            '''
            dbConn.deleteContact(contact_id)

            logger.log('Redirecting to admin page')
            return redirect(url_for('admin_project_management_contacts'))

        @app.route('/admin/data')
        @login_required
        def data():
            '''
            Routes the user to the Data Page of the website
            '''

            # get unread messages
            unreadRequests = dbConn.getRequests(unread=True)
            unreadQuestions = dbConn.getQuestions(unread=True)

            # get data for front-end presentation
            admins = dbConn.getAdmins()
            requests = dbConn.getRequests()
            images = dbConn.getImages()
            layouts = dbConn.getLayouts()
            questions = dbConn.getQuestions()
            contacts = dbConn.getContacts()
            products = dbConn.getProducts()
            visitors = dbConn.getVisitors()

            logger.log('Serving admin data page')
            return render_template('admin/data.html',
                                   title='Admin: Data',
                                   admins=admins,
                                   requests=requests,
                                   images=images,
                                   layouts=layouts,
                                   questions=questions,
                                   contacts=contacts,
                                   products=products,
                                   visitors=visitors,
                                   unreadRequests=unreadRequests,
                                   unreadQuestions=unreadQuestions)

        @app.route('/admin/project-management/requests')
        @login_required
        def admin_project_management_requests():
            '''
            Routes the user to the Requests Management page of the website
            '''

            # get unread messages
            unreadRequests = dbConn.getRequests(unread=True)
            unreadQuestions = dbConn.getQuestions(unread=True)

            # get data to be used in page
            requests = dbConn.getRequests(order_id=True)

            logger.log('Serving Project Management page')
            return render_template('admin/project-management-requests.html',
                                   title='Admin: Project Management',
                                   requests=requests,
                                   unreadRequests=unreadRequests,
                                   unreadQuestions=unreadQuestions)

        @app.route('/admin/project-management/questions')
        @login_required
        def admin_project_management_questions():
            '''
            Routes the user to the Questions Management page of the website
            '''

            # get unread messages
            unreadRequests = dbConn.getRequests(unread=True)
            unreadQuestions = dbConn.getQuestions(unread=True)

            # get data to be used in page
            questions = dbConn.getQuestions(order_id=True)

            logger.log('Serving Project Management page')
            return render_template('admin/project-management-questions.html',
                                   title='Admin: Project Management',
                                   questions=questions,
                                   unreadRequests=unreadRequests,
                                   unreadQuestions=unreadQuestions)

        @app.route('/admin/project-management/contacts')
        @login_required
        def admin_project_management_contacts():
            '''
            Routes the user to the Contacts Management page of the website
            '''

            # get unread messages
            unreadRequests = dbConn.getRequests(unread=True)
            unreadQuestions = dbConn.getQuestions(unread=True)

            # get data to be used in page
            contacts = dbConn.getContacts(order_id=True)

            logger.log('Serving Project Management page')
            return render_template('admin/project-management-contacts.html',
                                   title='Admin: Project Management',
                                   contacts=contacts,
                                   unreadRequests=unreadRequests,
                                   unreadQuestions=unreadQuestions)

        @app.route('/admin/product-management')
        @login_required
        def admin_product_management():
            '''
            Routes the user to the Admin Product Management page of the website
            '''

            # get unread messages
            unreadRequests = dbConn.getRequests(unread=True)
            unreadQuestions = dbConn.getQuestions(unread=True)

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
                productsFeaturedImages=productsFeaturedImages,
                unreadRequests=unreadRequests,
                unreadQuestions=unreadQuestions
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

            # update product
            dbConn.updateProduct(
                id=product_id, name=product_name,
                description=product_description,
                is_featured_product=is_featured_product)

            logger.log('Redirecting to admin page')
            return redirect(url_for('admin_product_management'))

        @app.route('/admin/product-management/updateImages/<product_id>',
                   methods=['POST'])
        @login_required
        def admin_product_updateImages_productid(product_id):
            '''
            Add a new image to a product or delete images
            '''

            # add new images
            images = request.files.getlist('addImages[]')
            for image in images:
                if image.filename:
                    path = app.config['AWS_LOCAL_IMAGE_PATH']
                    timestamp = helper.getTimestamp(datetime.now())
                    filename = f'{timestamp}_{image.filename}'
                    filelocation = f'{path}/{filename}'
                    location = f'../static/images/{filename}'
                    image.save(filelocation)
                    dbConn.setImage(location, product_id)
                    logger.log(f'Saving image {image.filename}')

            # delete images
            images = request.form.getlist('deleteImages[]')
            for image in images:
                dbConn.deleteImage(image)

            # update Featured image
            try:
                image_id = request.form['replaceImage']
                dbConn.makeFeaturedImage(image_id)
            except BadRequestKeyError:
                # ignore if user hasn't passed a replacement image
                pass

            logger.log('Redirecting to admin page')
            return redirect(url_for('admin_product_management'))

        @app.route('/admin/product-management/delete/<product_id>',
                   methods=['POST'])
        @login_required
        def admin_product_delete_productid(product_id):
            '''
            Delete a Product based on modal input
            '''
            # get product and associated images
            product = dbConn.getProduct(id=product_id)
            productImages = dbConn.getJoined_ProductImages(name=product.name)

            # delete the images
            for productImage in productImages:
                dbConn.deleteImage(id=productImage.image_id)

            # Delete the product
            dbConn.deleteProduct(id=product_id)

            logger.log('Redirecting to admin page')
            return redirect(url_for('admin_product_management'))

        @app.route('/admin/product-management/new-product',
                   methods=['POST'])
        @login_required
        def admin_product_newproduct():
            '''
            Create a new product
            '''

            # get form data
            name = request.form['productName']
            description = request.form['productDescription']
            image = request.files['featuredImage']

            # handle is_featured_product
            try:
                is_featured_product = request.form['is_featured_product']
                is_featured_product = True
            except BadRequestKeyError:
                is_featured_product = False

            # add new product
            product = dbConn.setProduct(name, description, is_featured_product)

            # add image
            path = app.config['AWS_LOCAL_IMAGE_PATH']
            timestamp = helper.getTimestamp(datetime.now())
            filename = f'{timestamp}_{image.filename}'
            filelocation = f'{path}/{filename}'
            location = f'../static/images/{filename}'
            image.save(filelocation)
            image = dbConn.setImage(location, product.id, is_featured_img=True)

            return redirect(url_for('admin_product_management'))

        @app.route('/admin/site-management')
        @login_required
        def admin_site_management():
            '''
            Routes a user to the Site Management part of the Admin Dashboard
            '''

            # get unique visitors per month
            visitorsPerMonth = dbConn.getVisitorsPerMonth(exclude_admins=True)

            # total number of unique Visitors and only this month's
            date = datetime.now().strftime('%b %Y')
            totalVisitors = 0
            totalVisitorsThisMonth = 0
            for label, data in visitorsPerMonth:
                totalVisitors += data
                if label == date:
                    totalVisitorsThisMonth = data

            # get unread messages
            unreadRequests = dbConn.getRequests(unread=True)
            unreadQuestions = dbConn.getQuestions(unread=True)

            # get layout information
            layouts = dbConn.getLayouts(order_id=True)

            # get locations for dynamic site rendering
            locations = list(set([layout.location for layout in layouts]))

            return render_template(
                'admin/site-management.html',
                title='Site Management',
                layouts=layouts,
                locations=locations,
                totalVisitors=totalVisitors,
                totalVisitorsThisMonth=totalVisitorsThisMonth,
                unreadRequests=unreadRequests,
                unreadQuestions=unreadQuestions
                )

        @app.route('/admin/site-management/update-layout/<layout_id>',
                   methods=['POST'])
        @login_required
        def admin_site_management_update(layout_id):
            '''
            Update the layout content at the given layout id
            '''

            # get form data and update the layout content
            content = request.form['layout-content']
            dbConn.updateLayout(layout_id, content)

            return redirect(url_for('admin_site_management'))
