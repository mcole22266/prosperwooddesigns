# DbConnector.py
# Michael Cole
#
# Simplifies communicating with the database
# ------------------------------------------

from datetime import datetime

from .Logger import Logger
from app.extensions.Helper import Helper

# Instantiate variables
logger = Logger()
helper = Helper()


class DbConnector:
    '''
    DbConnector object to be used in other files in order to simplify
    communication with the db
    '''

    def __init__(self):
        '''
        Instantiate DbConnector with the SQLAlchemy db object created
        in models.py
        '''
        from app.models import db
        self.db = db

    def getAdmins(self):
        '''
        Return all Admin rows
        '''
        from app.models import Admin
        return Admin.query.all()

    def getAdmin(self, username=False, id=False):
        '''
        Return a single Admin row based on the following parameters:

        username (str): Set to return a row based on a given username
        id (int): Set to return a row based on a given id
        '''
        from app.models import Admin
        if username:
            return Admin.query.filter_by(username=username).first()
        if id:
            return Admin.query.filter_by(id=id).first()

    def setAdmin(self, username, password, firstname, lastname,
                 created_date=datetime.now(), commit=True):
        '''
        Create an Admin row in the admin table
        '''
        import flask_bcrypt
        from app.models import Admin

        # Encrypt the given password before storing
        encrypted_password = flask_bcrypt.generate_password_hash(
            password).decode('utf-8')
        admin = Admin(username, encrypted_password, firstname, lastname,
                      created_date=created_date)
        self.db.session.add(admin)
        if commit:
            self.db.session.commit()
        logger.log(f'Created admin - {admin}')
        return admin

    def getRequests(self, order_id=False, unread=False,
                    complete=False):
        '''
        Get all Request rows from the database.

        order_id (bool): Set True to "order by id desc"
        unread (bool): Set True to only return unread requests
        complete (bool): Set True to only return completed requests
        '''
        from app.models import Request
        if order_id:
            # order by id desc
            return Request.query.order_by(Request.id.desc())
        elif unread:
            return Request.query.filter_by(
                status='unread', is_archived=False
                ).order_by(Request.created_date.desc()).all()
        elif complete:
            return Request.query.filter_by(
                status='complete'
            ).all()
        else:
            return Request.query.all()

    def getRequest(self, id=False):
        '''
        Get a single Request row based on the following parameter:

        id (int): Set to get a Request by id
        '''
        from app.models import Request
        if id:
            return Request.query.filter_by(id=id).first()

    def setRequest(self, emailaddress, phonenumber, name, contactmethod,
                   description, how_hear, status='unread', is_archived=False,
                   created_date=datetime.now(),
                   commit=True):
        '''
        Create a Request row
        '''
        from app.models import Request
        request = Request(emailaddress, phonenumber, name, contactmethod,
                          description, how_hear, status, is_archived,
                          created_date)
        self.db.session.add(request)
        if commit:
            self.db.session.commit()
        logger.log(f'Created Request - {request}')
        return request

    def updateRequest(self, id, status=False, is_archived=False,
                      commit=True):
        '''
        Update a Request row based on the following parameters:

        status (str): Set to change the status of a Request
        is_archived (bool): Set True to change the is_archived of a Request
        '''
        request = self.getRequest(id=id)
        if status:
            request.status = status
            logger.log(
                f'Updated Request {request.id} status to {status}'
            )
        if is_archived:
            request.is_archived = is_archived
            logger.log(
                f'Updated Request {request.id} - now archived'
            )
        if commit:
            self.db.session.commit()

    def deleteRequest(self, id, commit=True):
        '''
        Delete a Request row by id
        '''
        request = self.getRequest(id=id)

        self.db.session.delete(request)
        logger.log(f'Deleted Request - {request}')
        if commit:
            self.db.session.commit()

    def getImages(self, featured=False):
        '''
        Get all Image rows from the db

        featured (bool): Set True to return only featured images
        '''
        from app.models import Image
        if featured:
            return Image.query.filter_by(featured=True).all()
        else:
            return Image.query.all()

    def getImage(self, id=False):
        '''
        Get a single Image row based on the following parameter:

        id (int): Set to return an image based on a given id
        '''
        from app.models import Image
        if id:
            return Image.query.filter_by(id=id).first()

    def setImage(self, location, product_id, is_featured_img=False,
                 created_date=datetime.now(),
                 commit=True):
        '''
        Create an Image in the db
        '''
        from app.models import Image
        image = Image(location, product_id, is_featured_img, created_date)
        self.db.session.add(image)
        if commit:
            self.db.session.commit()
        logger.log(f'Created Image - {image}')
        return image

    def updateImage(self, id, is_featured_img,
                    commit=True):
        '''
        Update an Image row based on the following parameters:

        is_featured_img (bool): Set to change the is_featured_img of the Image
        '''
        # get image
        image = self.getImage(id=id)

        # Set is_featured_img
        image.is_featured_img = is_featured_img

        logger.log(
            f'Updated Image {image.id} - to {is_featured_img}'
        )
        if commit:
            self.db.session.commit()

    def deleteImage(self, id, commit=True):
        '''
        Delete an Image row by id
        '''
        image = self.getImage(id=id)

        self.db.session.delete(image)
        logger.log(f'Deleted Image - {image}')
        if commit:
            self.db.session.commit()

        return image

    def getProducts(self):
        '''
        Get all Product rows from the db
        '''
        from app.models import Product
        return Product.query.all()

    def getProduct(self, id=False, name=False):
        '''
        Get a single Product row based on the following parameter:

        id (int): Set to return a row based on id
        name (str): Set to return a row based on name
        '''
        from app.models import Product
        if id:
            return Product.query.filter_by(id=id).first()
        if name:
            return Product.query.filter_by(name=name).first()

    def setProduct(self, name, description, is_featured_product=False,
                   created_date=datetime.now(), commit=True):
        '''
        Create a Product row
        '''
        from app.models import Product
        product = Product(name, description, is_featured_product,
                          created_date=created_date)
        self.db.session.add(product)
        if commit:
            self.db.session.commit()
        logger.log(f'Created Product - {product}')
        return product

    def updateProduct(self, id, name=False, description=False,
                      is_featured_product=False, commit=True):
        '''
        Update a Product row based on the following parameters:

        name (str): Set to change the name of a Product
        description (str): Set to change the description of a Product
        is_featured_product (bool): Set True to change the
            is_featured_product of a Product
        '''
        product = self.getProduct(id=id)
        if name:
            product.name = name
            logger.log(
                f'Updated Product {product.id} name to {name}'
            )
        if description:
            product.description = description
            product.description_html = helper.to_html(description)
            logger.log(
                f'Updated Product {product.id} description to {description}'
            )
        # always update is_featured_product since it is boolean
        product.is_featured_product = is_featured_product
        logger.log(
            f'Updated Product {product.id} is_featured_product to \
{is_featured_product}'
        )
        if commit:
            self.db.session.commit()

    def deleteProduct(self, id, commit=True):
        '''
        Delete a Product row by id
        '''
        product = self.getProduct(id=id)

        self.db.session.delete(product)
        logger.log(f'Deleted Product - {product}')
        if commit:
            self.db.session.commit()

    def getLayouts(self, location=False, order_id=False):
        '''
        Get all Layout rows from the db

        Parameters:
            location (str): Pass to return only rows with pass location
            order_id (bool): Set True to order rows by id
        '''
        from app.models import Layout
        if location:
            return Layout.query.filter_by(location=location).all()
        if order_id:
            return Layout.query.order_by(Layout.id).all()
        return Layout.query.all()

    def getLayout(self, id=False):
        '''
        Get a single Layout row based on the following parameter:

        Parameters:
            id (int): Set to return a row based on id
        '''
        from app.models import Layout
        if id:
            return Layout.query.filter_by(id=id).first()

    def setLayout(self, location, name, content,
                  commit=True):
        '''
        Create a Layout row
        '''
        from app.models import Layout
        layout = Layout(location, name, content)
        self.db.session.add(layout)
        if commit:
            self.db.session.commit()
        logger.log(f'Created Layout - {layout}')
        return layout

    def updateLayout(self, id, content,
                     commit=True):
        '''
        Update a Layout row based on the following parameters:

        id (int): The id you want to update
        '''
        layout = self.getLayout(id=id)
        layout.content = content
        layout.content_html = helper.to_html(content)
        logger.log(
            f'Updated Layout {layout.id} content'
        )
        if commit:
            self.db.session.commit()

    def getQuestions(self, order_id=False, unread=False):
        '''
        Get all Question rows

        order_id (bool): Set True to "order by id desc"
        unread (bool): Set True to get only unread questions
        '''
        from app.models import Question
        if order_id:
            # order by id desc
            return Question.query.order_by(Question.id.desc())
        elif unread:
            return Question.query.filter_by(
                status='unread', is_archived=False
                ).order_by(Question.created_date.desc()).all()
        else:
            return Question.query.all()

    def getQuestion(self, id=False):
        '''
        Get a single Question row based on the following parameter:

        id (int): Set to get row by id
        '''
        from app.models import Question
        if id:
            return Question.query.filter_by(id=id).first()

    def setQuestion(self, emailaddress, name, content, how_hear,
                    status='unread', is_archived=False,
                    created_date=datetime.now(),
                    commit=True):
        '''
        Create a Question row
        '''
        from app.models import Question
        question = Question(emailaddress, name, content, how_hear, status,
                            is_archived, created_date)
        self.db.session.add(question)
        if commit:
            self.db.session.commit()
        logger.log(f'Created Question - {question}')
        return question

    def updateQuestion(self, id, status=False, is_archived=False,
                       commit=True):
        '''
        Update a Question row based on the following parameters:

        id (int): The id you want to update
        status (str): Set to update the status
        is_archived (bool): Set to update the is_archived
        '''
        question = self.getQuestion(id=id)
        if status:
            question.status = status
            logger.log(
                f'Updated Question {question.id} status to {status}'
            )
        if is_archived:
            question.is_archived = is_archived
            logger.log(
                f'Updated Question {question.id} - Now archived'
            )
        if commit:
            self.db.session.commit()

    def deleteQuestion(self, id, commit=True):
        '''
        Delete a Question from the DB
        '''
        question = self.getQuestion(id=id)

        self.db.session.delete(question)
        logger.log(f'Deleted Question - {question}')
        if commit:
            self.db.session.commit()

    def getContacts(self, order_id=False):
        '''
        Get all Contact rows

        order_id (bool): Set True to "order by id desc"
        '''
        from app.models import Contact
        if order_id:
            # order by id desc
            return Contact.query.order_by(Contact.id.desc())
        else:
            return Contact.query.all()

    def getContact(self, id=False):
        '''
        Get a single Contact row based on the following parameter:

        id (int): Set to get row by id
        '''
        from app.models import Contact
        if id:
            return Contact.query.filter_by(id=id).first()

    def setContact(self, name, phonenumber=False, emailaddress=False,
                   commit=True):
        '''
        Create a Contact row
        '''
        from app.models import Contact
        contact = Contact(name, phonenumber, emailaddress)
        self.db.session.add(contact)
        if commit:
            self.db.session.commit()
        logger.log(f'Created Contact - {contact}')
        return contact

    def deleteContact(self, id, commit=True):
        '''
        Delete a Contact from the DB
        '''
        contact = self.getContact(id=id)

        self.db.session.delete(contact)
        logger.log(f'Deleted Contact - {contact}')
        if commit:
            self.db.session.commit()

    def getVisitors(self, order_id=False, order_num_visits=False,
                    exclude_admins=False):
        '''
        Get all Visitor rows

        order_id (bool): Set True to "order by id desc"
        order_num_visits (bool): Set True to "order by num_visits desc"
        exclude_admins (bool): Set True to ignore all admin visitors
        '''
        from app.models import Visitor
        if order_id:
            # order by id desc
            return Visitor.query.order_by(Visitor.id.desc()).all()
        if order_num_visits:
            # order by num_visits desc
            return Visitor.query.order_by(Visitor.num_visits.desc()).all()
        if exclude_admins:
            return Visitor.query.filter_by(is_admin=False).all()
        else:
            return Visitor.query.all()

    def getVisitor(self, id=False, ipaddress=False):
        '''
        Get a single Visitor row based on the following parameter:

        id (int): Set to get row by id
        '''
        from app.models import Visitor
        if id:
            return Visitor.query.filter_by(id=id).first()
        if ipaddress:
            return Visitor.query.filter_by(ipaddress=ipaddress).first()

    def setVisitor(self, ipaddress, first_visit_date=datetime.now(),
                   most_recent_visit_date=datetime.now(), num_visits=1,
                   is_admin=False, commit=True):
        '''
        Create a Visitor row
        '''
        from app.models import Visitor

        # if visitor already exists, update most_recent_visit_date and
        # num_visits
        visitor = self.getVisitor(ipaddress=ipaddress)
        if visitor:
            visitor.most_recent_visit_date = datetime.now()
            visitor.num_visits += 1
            # change don't touch is_admin if it is True
            if not visitor.is_admin:
                visitor.is_admin = is_admin
        # if visitor does not exist, create a new one
        else:
            visitor = Visitor(
                ipaddress, first_visit_date, most_recent_visit_date,
                num_visits, is_admin
                )
            self.db.session.add(visitor)

        if commit:
            self.db.session.commit()
        logger.log(f'Created Visitor - {visitor}')
        return visitor

    def setJoined_ProductImage(self, product_name, product_description,
                               image_location, is_featured_product=False,
                               is_featured_img=False,
                               created_date=datetime.now(), commit=True):
        '''
        Create an image object. If the given product already exists, the image
        object will simply point to that product id. If the given product does
        not yet exist, the product will be created first using the given
        values.

        Returns tuple: (product, image)
        '''

        product = self.getProduct(name=product_name)

        # check for product availability
        if not product:
            # Create the product if it does not yet exist
            product = self.setProduct(product_name, product_description,
                                      is_featured_product=is_featured_product,
                                      created_date=created_date, commit=commit)

        # create the image pointing at the product
        image = self.setImage(image_location, product.id,
                              is_featured_img=is_featured_img,
                              created_date=created_date, commit=commit)

        return (product, image)

    def getJoined_ProductImages(self, name=False, featuredImages=False,
                                featuredProducts=False):
        '''
        Return all rows where image.product_id=product.id

        name (str): Set to only return all product/images by name
        featuredImages (bool): Set to only return all product/images with
            featured images
        featuredProducts (bool): Set to only return all product/images that
            are featured products
        '''

        if name:
            # return only product/images where product_name=name
            result = self.db.session.execute(f'''
SELECT DISTINCT
    product.id, product.name, product.description, product.description_html,
    product.is_featured_product,
    image.location, image.is_featured_img, image.id AS image_id
FROM product
    JOIN image ON image.product_id=product.id
WHERE product.name='{name}'
ORDER BY image.is_featured_img DESC
''')

        elif featuredImages:
            # return only featured product/images
            result = self.db.session.execute('''
SELECT DISTINCT
    product.id, product.name, product.description, product.description_html,
    product.is_featured_product,
    image.location, image.is_featured_img, image.id AS image_id
FROM product
    JOIN image ON image.product_id=product.id
WHERE image.is_featured_img='y'
ORDER BY image.is_featured_img DESC, product.name
''')
        elif featuredProducts:
            # return only featured product/images
            result = self.db.session.execute('''
SELECT DISTINCT
    product.id, product.name, product.description, product.description_html,
    product.is_featured_product,
    image.location, image.is_featured_img, image.id AS image_id
FROM product
    JOIN image ON image.product_id=product.id
WHERE product.is_featured_product='y'
    AND image.is_featured_img='y'
''')
        else:
            # return all product/images
            result = self.db.session.execute('''
SELECT DISTINCT
    product.id, product.name, product.description, product.description_html,
    product.is_featured_product,
    image.location, image.is_featured_img, image.id AS image_id
FROM product
    JOIN image ON image.product_id=product.id
ORDER BY image.is_featured_img DESC, product.name
''')
        productImages = []
        for item in result:
            # return as a list of ProductImage objects
            # (defined in this file)
            productImage = ProductImage(item[0], item[1], item[2], item[3],
                                        item[4], item[5], item[6], item[7])
            productImages.append(productImage)

        return productImages

    def makeFeaturedImage(self, image_id):
        '''
        Make the given image the featured image for it's product
        '''
        # get the image and associated product
        image = self.getImage(id=image_id)
        product = self.getProduct(id=image.product_id)

        # get all featured images
        productImages = self.getJoined_ProductImages(featuredImages=True)

        # set the current product's featured image as False
        for productImage in productImages:
            if productImage.name == product.name:
                # get the featured image
                prevFeatured = self.getImage(id=productImage.image_id)
                self.updateImage(prevFeatured.id, is_featured_img=False)

        # make the new image a featured image
        self.updateImage(image.id, is_featured_img=True)

    def getVisitorsPerMonth(self, exclude_admins=False):
        '''
        Returns the number of unique visitors per month
        '''

        if exclude_admins:
            where_clause = "WHERE is_admin='f'"
        else:
            where_clause = ''

        result = self.db.session.execute(f'''
SELECT
    DATE_PART('year', most_recent_visit_date) AS year,
    DATE_PART('month', most_recent_visit_date) AS month,
    COUNT(ipaddress) AS num_visitors
FROM visitor
{where_clause}
GROUP BY year, month
ORDER BY year, month
''')
        visitorsPerMonth = []
        for item in result:
            # return as a list of tuples
            year, month, num_visitors = item
            date = datetime(int(year), int(month), 1).strftime('%b %Y')
            visitorsPerMonth.append(
                (date, num_visitors)
                )

        return visitorsPerMonth

    def getMarketingStats(self):
        '''
        Returns the how_hear count from both the Request Form and
        Question Form
        '''

        results = self.db.session.execute('''
WITH
    results AS (
        SELECT
            how_hear
        FROM request
        UNION ALL
        SELECT
            how_hear
        FROM question
    )
SELECT
    CASE
        WHEN how_hear IN (
            'Facebook', 'Instagram', 'Ad',
            'No Response', 'Word of Mouth'
        )
        THEN how_hear
        ELSE 'Other'
    END AS source,
    count(*) AS num
FROM results
GROUP BY source
ORDER BY source
''')

        marketingStats = []
        for how_hear, num in results:
            marketingStats.append(
                (how_hear, num)
            )

        return marketingStats


class ProductImage:
    '''
    Object to represent ProductImage results returned by
    getJoined_ProductImages. Allow for easier use
    '''

    def __init__(self, id, name, description, description_html,
                 is_featured_product, location, is_featured_img,
                 image_id):
        self.id = id
        self.name = name
        self.description = description
        self.description_html = description_html
        self.is_featured_product = is_featured_product
        self.location = location
        self.is_featured_img = is_featured_img
        self.image_id = image_id
