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

    def loadAdmin(self, db, num_rows=3):
        '''
        Load Admin table with fake data
        '''
        from .models import Admin

        for i in range(num_rows):
            username = self.fake.user_name()
            password = self.fake.password()
            firstname = self.fake.first_name()
            lastname = self.fake.last_name()
            startdate = datetime.fromisoformat('2020-01-01')
            enddate = datetime.now()
            created_date = self.fake.date_between(startdate, enddate)
            admin = Admin(
                username, password, firstname,
                lastname, created_date
                )
            db.session.add(admin)
        db.session.commit()
