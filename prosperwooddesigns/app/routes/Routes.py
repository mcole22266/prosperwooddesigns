# Routes.py
# Michael Cole
#
# Defines all app's main routing logic
# --------------------------------

from flask import redirect, render_template, request, url_for
from werkzeug.exceptions import BadRequestKeyError

from app.extensions.DbConnector import DbConnector
from app.extensions.Helper import Helper
from app.extensions.Logger import Logger
from flask_login import login_user

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

            # log user in automatically if set
            if app.config['ADMIN_AUTO_LOGIN']:
                from flask_login import current_user
                admin = dbConn.getAdmin(
                    username=app.config['DB_TEST_ADMIN_USERNAME']
                    )
                login_user(admin)
                logger.log(f'Logged in {current_user}')

            # get all featured products
            featuredProducts = dbConn.getJoined_ProductImages(
                featuredProducts=True)

            logger.log('Serving index page')
            return render_template('index.html',
                                   title='Home',
                                   featuredProducts=featuredProducts)

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
            joinedProductsImages = dbConn.getJoined_ProductImages(
                featuredImages=True
                )
            # chunk into lists of no greater than 4
            joinedProductsImages = helper.chunk(joinedProductsImages, 4)
            return render_template('designs.html',
                                   title='Designs',
                                   joinedProductsImages=joinedProductsImages)

        @app.route('/designs/<product_name>')
        def designs_product(product_name):
            '''
            Routes the user to the Product Page of a chosen design
            '''
            logger.log(f'Serving {product_name} product page')

            joinedProductsImages = dbConn.getJoined_ProductImages(
                name=product_name)

            return render_template('designs_product.html',
                                   title=f'{product_name}',
                                   joinedProductsImages=joinedProductsImages)

        @app.route('/requestform', methods=['GET', 'POST'])
        def requestform():
            '''
            Routes the user to the Request Form of the website
            '''
            from app.forms import RequestForm

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

            try:
                product = request.args['product']
            except BadRequestKeyError:
                product = None

            logger.log('Serving request form page')
            return render_template('requestform.html',
                                   title='Request Form',
                                   requestform=requestform,
                                   product=product)

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
            from app.forms import QuestionForm

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

            try:
                product = request.args['product']
            except BadRequestKeyError:
                product = None

            logger.log('Serving question form page')
            return render_template('questionform.html',
                                   title='Question Form',
                                   questionform=questionform,
                                   product=product)

        @app.route('/questionform/success')
        def questionform_success():
            '''
            Routes the user to a confirmation page after submitting a
            question form
            '''
            logger.log('Serving question form success page')
            return render_template('questionform_success.html',
                                   title='Question Success')
