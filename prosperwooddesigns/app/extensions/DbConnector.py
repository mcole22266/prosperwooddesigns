# DbConnector.py
# Michael Cole
#
# Simplifies communicating with the database
# ------------------------------------------

from datetime import datetime

from .Logger import Logger

# Instantiate variables
logger = Logger()


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
        from app.models import Admin
        import flask_bcrypt

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

    def getRequests(self, order_id=False):
        '''
        Get all Request rows from the database.

        order_id (bool): Set True to "order by id desc"
        '''
        from app.models import Request
        if order_id:
            # order by id desc
            return Request.query.order_by(Request.id.desc())
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

    def getLayouts(self):
        '''
        Get all Layout rows from the db
        '''
        from app.models import Layout
        return Layout.query.all()

    def getLayout(self, id=False):
        '''
        Get a single Layout row based on the following parameter:

        id (int): Set to return a row based on id
        '''
        from app.models import Layout
        if id:
            return Layout.query.filter_by(id=id).first()

    def setLayout(self, endpoint, content_name, content, is_image,
                  created_date, commit=True):
        '''
        Create a Layout row
        '''
        from app.models import Layout
        layout = Layout(endpoint, content_name, content, is_image,
                        created_date=datetime.now())
        self.db.session.add(layout)
        if commit:
            self.db.session.commit()
        logger.log(f'Created Layout - {layout}')
        return layout

    def getQuestions(self, order_id=False):
        '''
        Get all Question rows

        order_id (bool): Set True to "order by id desc"
        '''
        from app.models import Question
        if order_id:
            # order by id desc
            return Question.query.order_by(Question.id.desc())
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

        name (bool): Set to only return all product/images by name
        featuredImages (bool): Set to only return all product/images with
            featured images
        featuredProducts (bool): Set to only return all product/images that
            are featured products
        '''

        if name:
            # return only product/images where product_name=name
            result = self.db.session.execute(f'''
SELECT
    product.id, product.name, product.description, product.is_featured_product,
    image.location, image.is_featured_img
FROM product
    JOIN image ON image.product_id=product.id
WHERE product.name='{name}'
ORDER BY image.is_featured_img DESC
''')

        elif featuredImages:
            # return only featured product/images
            result = self.db.session.execute('''
SELECT DISTINCT
    product.id, product.name, product.description, product.is_featured_product,
    image.location, image.is_featured_img
FROM product
    JOIN image ON image.product_id=product.id
WHERE image.is_featured_img='y'
ORDER BY product.name
''')
        elif featuredProducts:
            # return only featured product/images
            result = self.db.session.execute('''
SELECT DISTINCT
    product.id, product.name, product.description, product.is_featured_product,
    image.location, image.is_featured_img
FROM product
    JOIN image ON image.product_id=product.id
WHERE product.is_featured_product='y'
    AND image.is_featured_img='y'
''')
        else:
            # return all product/images
            result = self.db.session.execute('''
SELECT
    product.id, product.name, product.description, product.is_featured_product,
    image.location, image.is_featured_img
FROM product
    JOIN image ON image.product_id=product.id
ORDER BY product.name
''')
        productImages = []
        for item in result:
            # return as a list of ProductImage objects
            # (defined in this file)
            productImage = ProductImage(item[0], item[1], item[2], item[3],
                                        item[4], item[5])
            productImages.append(productImage)

        return productImages


class ProductImage:
    '''
    Object to represent ProductImage results returned by
    getJoined_ProductImages. Allow for easier use
    '''

    def __init__(self, id, name, description, is_featured_product,
                 location, is_featured_img):
        self.id = id
        self.name = name
        self.description = description
        self.is_featured_product = is_featured_product
        self.location = location
        self.is_featured_img = is_featured_img
