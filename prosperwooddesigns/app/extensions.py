# extensions.py
# Michael Cole

# Collection of extensions to be used throughout the app
# ------------------------------------------------------

import sys
import os
from datetime import datetime

import boto3


class Logger:
    '''
    Logger object used to print to the console as well
    as log to a file in development
    '''

    def log(self, string, loc='stdout'):
        '''
        Prints to the console by default. Can pass a filename
        for logs to write to
        '''

        if loc == 'stdout':
            print(f'>> {string}', file=sys.stdout, flush=True)
        else:
            print(f'>> {string}', file=loc, flush=True)


class DbConnector:

    def __init__(self):
        from .models import db
        self.db = db
        self.logger = Logger()

    def getAdmins(self):
        from .models import Admin
        return Admin.query.all()

    def getAdmin(self, username=False, id=False):
        from .models import Admin
        if username:
            return Admin.query.filter_by(username=username).first()
        if id:
            return Admin.query.filter_by(id=id).first()

    def setAdmin(self, username, password, firstname, lastname,
                 created_date=datetime.now(), commit=True):
        from .models import Admin
        admin = Admin(username, password, firstname, lastname,
                      created_date=created_date)
        self.db.session.add(admin)
        if commit:
            self.db.session.commit()
        self.logger.log(f'Created admin - {admin}')
        return admin

    def getRequests(self):
        from .models import Request
        return Request.query.all()

    def getRequest(self, id=False):
        from .models import Request
        if id:
            return Request.query.filter_by(id=id).first()

    def setRequest(self, emailaddress, phonenumber, name, contactmethod,
                   description, status, is_deleted,
                   created_date=datetime.now(), commit=True):
        from .models import Request
        request = Request(emailaddress, phonenumber, name, contactmethod,
                          description, status, is_deleted, created_date)
        self.db.session.add(request)
        if commit:
            self.db.session.commit()
        self.logger.log(f'Created Request - {request}')
        return request

    def getImages(self):
        from .models import Image
        return Image.query.all()

    def getImage(self, id=False):
        from .models import Image
        if id:
            return Image.query.filter_by(id=id).first()

    def setImage(self, name, description, filename,
                 created_date=datetime.now(),
                 commit=True):
        from .models import Image
        image = Image(name, description, filename, created_date)
        self.db.session.add(image)
        if commit:
            self.db.session.commit()
        self.logger.log(f'Created Image - {image}')
        return image

    def getLayouts(self):
        from .models import Layout
        return Layout.query.all()

    def getLayout(self, id=False):
        from .models import Layout
        if id:
            return Layout.query.filter_by(id=id).first()

    def setLayout(self, endpoint, content_name, content, is_image,
                  created_date, commit=True):
        from .models import Layout
        layout = Layout(endpoint, content_name, content, is_image,
                        created_date=datetime.now())
        self.db.session.add(layout)
        if commit:
            self.db.session.commit()
        self.logger.log(f'Created Layout - {layout}')
        return layout

    def getContacts(self):
        from .models import Contact
        return Contact.query.all()

    def getContact(self, id=False):
        from .models import Contact
        if id:
            return Contact.query.filter_by(id=id).first()

    def setContact(self, emailaddress, name, content,
                   created_date=datetime.now(),
                   commit=True):
        from .models import Contact
        contact = Contact(emailaddress, name, content, created_date)
        self.db.session.add(contact)
        if commit:
            self.db.session.commit()
        self.logger.log(f'Created Contact - {contact}')
        return contact


class S3Connecter:
    '''
    S3 Connector to be used specifically for interacting with
    this project's S3 Bucket
    '''

    def __init__(self):
        '''
        Initializes by connecting to S3
        '''
        self.S3ImageBucket = os.environ['AWS_PROJECT_BUCKET']
        self.S3ImageFolder = os.environ['AWS_PROJECT_BUCKET_IMAGE_DIR']
        self.LocalImagePath = os.environ['AWS_LOCAL_IMAGE_PATH']

        # connect to S3
        self.s3Client = boto3.client('s3')
        self.s3Resource = boto3.resource('s3')

    def uploadImages(self):
        '''
        Uploads all images in the images directory of this project
        '''
        logger = Logger()
        self.images = [f for f in os.listdir(self.LocalImagePath)]
        for imageName in self.images:
            self.s3Client.upload_file(
                f'{self.LocalImagePath}/{imageName}',  # local image name
                self.S3ImageBucket,  # bucket name
                f'{self.S3ImageFolder}{imageName}')  # remote image name
            logger.log(f'**Uploaded {imageName} to S3**')
        logger.log('Done')

    def downloadImages(self):
        '''
        Downloads all images from the S3 bucket into the images directory
        of this project
        '''
        logger = Logger()
        bucket = self.s3Resource.Bucket(self.S3ImageBucket)
        objects = bucket.objects.filter(Prefix=self.S3ImageFolder)
        for obj in objects:
            path, filename = os.path.split(obj.key)
            if filename != '':
                bucket.download_file(
                    obj.key,
                    f'{self.LocalImagePath}/{filename}')
                logger.log(f'**Downloaded {filename} from S3**')
        logger.log('Done')


class MockData:
    '''
    Loads database with mock data for developing and testing
    '''
    from faker import Faker

    fake = Faker()
    dbConn = DbConnector()

    def fakeDate(
        self,
        startdate=datetime.fromisoformat('2020-01-01'),
        enddate=datetime.now()
    ):
        '''
        Generate fake date for use in created_date
        '''

        return self.fake.date_between(startdate, enddate)

    def fakeDescription(
        self,
        num_paragraphs_min=2,
        num_paragraphs_max=5
    ):
        description = ''
        paragraphs = self.fake.paragraphs(self.fake.random_int(
            num_paragraphs_min, num_paragraphs_max
            )
        )
        for paragraph in paragraphs:
            description += f'{paragraph} '
        description = description[:-1]
        return description

    def hasData(self, db):
        '''
        Check if database is empty
        '''

        admins = self.dbConn.getAdmins()
        requests = self.dbConn.getRequests()
        images = self.dbConn.getImages()

        if len(admins) > 5 or len(requests) > 5 or len(images) > 5:
            return True
        return False

    def loadAdmin(self, db, num_rows=3):
        '''
        Load Admin table with fake data
        '''

        for i in range(num_rows):
            username = self.fake.user_name()
            password = self.fake.password()
            firstname = self.fake.first_name()
            lastname = self.fake.last_name()
            created_date = self.fakeDate()

            self.dbConn.setAdmin(username, password, firstname, lastname,
                                 created_date, commit=False)
        db.session.commit()

    def loadRequest(self, db, num_rows=8):
        '''
        Load Request table with fake data
        '''

        for i in range(num_rows):
            emailaddress = self.fake.email()
            phonenumber = self.fake.phone_number()
            name = self.fake.name()
            contactmethod = self.fake.random_element([
                'phone', 'email', 'no preference'
            ])
            description = self.fakeDescription()
            status = self.fake.random_element([
                'unread', 'read', 'in progress', 'ready to deliver', 'complete'
            ])
            is_deleted = self.fake.boolean()
            created_date = self.fakeDate()

            self.dbConn.setRequest(emailaddress, phonenumber, name,
                                   contactmethod, description, status,
                                   is_deleted, created_date, commit=False)
        db.session.commit()

    def loadImage(self, db, num_rows=20):
        '''
        Load Image table with fake data
        '''

        for i in range(num_rows):
            name = self.fake.word()
            description = self.fakeDescription()
            filename = self.fake.file_path()
            created_date = self.fakeDate()

            self.dbConn.setImage(name, description, filename,
                                 created_date, commit=False)
        db.session.commit()

    def loadLayout(self, db, num_rows=30):
        '''
        Load Layout table with fake data
        '''

        for i in range(num_rows):
            endpoint = self.fake.uri_path()
            content_name = self.fake.word()
            content = self.fakeDescription(2, 3)
            is_image = self.fake.boolean()
            created_date = self.fakeDate()

            self.dbConn.setLayout(endpoint, content_name, content,
                                  is_image, created_date,
                                  commit=False)
        db.session.commit()

    def loadContact(self, db, num_rows=20):
        '''
        Load Contact table with fake data
        '''

        for i in range(num_rows):
            emailaddress = self.fake.email()
            name = self.fake.name()
            content = self.fakeDescription()
            created_date = self.fakeDate()

            self.dbConn.setContact(emailaddress, name, content,
                                   created_date, commit=False)
        db.session.commit()


class Helper:

    def getGreeting(self):
        from datetime import datetime
        import pytz

        utc_now = pytz.utc.localize(datetime.utcnow())
        ct_now = utc_now.astimezone(pytz.timezone('America/Chicago'))
        hour = ct_now.time().hour

        if hour >= 4 and hour <= 11:
            return 'Good Morning'
        elif hour >= 12 and hour <= 16:
            return 'Good Afternoon'
        elif hour >= 17 and hour <= 23:
            return 'Good Evening'
        else:
            return 'It is very late'
