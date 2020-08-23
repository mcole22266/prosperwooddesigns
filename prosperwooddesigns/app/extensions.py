# extensions.py
# Michael Cole

# Collection of extensions to be used throughout the app
# ------------------------------------------------------

import os
import sys
from datetime import datetime

from flask import current_app

import boto3


class Helper:

    def getGreeting(self):
        ct_now = self.getTime_tz()
        hour = ct_now.time().hour

        if hour >= 4 and hour <= 11:
            return 'Good Morning'
        elif hour >= 12 and hour <= 16:
            return 'Good Afternoon'
        elif hour >= 17 and hour <= 23:
            return 'Good Evening'
        else:
            return 'It is very late'

    def getTime_tz(self, tz='America/Chicago'):
        from datetime import datetime
        import pytz

        utc_now = pytz.utc.localize(datetime.now())
        return utc_now.astimezone(pytz.timezone(tz))


class Logger:
    '''
    Logger object used to print to the console as well
    as log to a file in development
    '''

    helper = Helper()

    def log(self, string):
        '''
        Prints to the console by default. Can pass a filename
        for logs to write to
        '''
        if current_app.config['LOG_TO_STDOUT']:
            print(f'>> {string}', file=sys.stdout, flush=True)

        if current_app.config['LOG_TO_FILE']:
            now = self.helper.getTime_tz()
            year = str(now.year).rjust(4, '0')
            month = str(now.month).rjust(2, '0')
            day = str(now.day).rjust(2, '0')
            hour = str(now.hour).rjust(2, '0')
            minute = str(now.minute).rjust(2, '0')
            second = str(now.second).rjust(2, '0')

            fileprefix = f'/prosperwooddesigns/logs/{year}/{month}'
            if not os.path.exists(fileprefix):
                os.makedirs(fileprefix)

            filename = f'{fileprefix}/log_{year}{month}{day}.log'
            timestamp = f'{hour}:{minute}:{second}'

            with open(filename, 'a+') as f:
                print(f'>> [{timestamp}] {string}', file=f, flush=True)


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
        import flask_bcrypt

        encrypted_password = flask_bcrypt.generate_password_hash(
            password).decode('utf-8')
        admin = Admin(username, encrypted_password, firstname, lastname,
                      created_date=created_date)
        self.db.session.add(admin)
        if commit:
            self.db.session.commit()
        self.logger.log(f'Created admin - {admin}')
        return admin

    def getRequests(self, order_date=False):
        from .models import Request
        if order_date:
            # order by created_date desc
            return Request.query.order_by(Request.created_date.desc())
        else:
            return Request.query.all()

    def getRequest(self, id=False):
        from .models import Request
        if id:
            return Request.query.filter_by(id=id).first()

    def setRequest(self, emailaddress, phonenumber, name, contactmethod,
                   description, status='unread', is_deleted=False,
                   created_date=datetime.now(), commit=True):
        from .models import Request
        request = Request(emailaddress, phonenumber, name, contactmethod,
                          description, status, is_deleted, created_date)
        self.db.session.add(request)
        if commit:
            self.db.session.commit()
        self.logger.log(f'Created Request - {request}')
        return request

    def updateRequest(self, id, status=False, commit=True):
        request = self.getRequest(id=id)
        if status:
            request.status = status
            self.logger.log(
                f'Updated Request {request.id} status to {status}'
            )
        if commit:
            self.db.session.commit()

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

    def getContacts(self, order_date=False):
        from .models import Contact
        if order_date:
            # order by created_date desc
            return Contact.query.order_by(Contact.created_date.desc())
        else:
            return Contact.query.all()

    def getContact(self, id=False):
        from .models import Contact
        if id:
            return Contact.query.filter_by(id=id).first()

    def setContact(self, emailaddress, name, content, status='unread',
                   created_date=datetime.now(),
                   commit=True):
        from .models import Contact
        contact = Contact(emailaddress, name, content, status, created_date)
        self.db.session.add(contact)
        if commit:
            self.db.session.commit()
        self.logger.log(f'Created Contact - {contact}')
        return contact

    def updateContact(self, id, status=False, commit=True):
        contact = self.getContact(id=id)
        if status:
            contact.status = status
            self.logger.log(
                f'Updated Contact {contact.id} status to {status}'
            )
        if commit:
            self.db.session.commit()


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
                'phone', 'email', None
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
            status = self.fake.random_element([
                'unread', 'read',
            ])
            created_date = self.fakeDate()

            self.dbConn.setContact(emailaddress, name, content, status,
                                   created_date, commit=False)
        db.session.commit()
