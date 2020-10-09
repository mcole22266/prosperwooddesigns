# S3Connector.py
# Michael Cole
#
# Used to simplify S3 connectivity
# --------------------------------

import os

import boto3

from .Logger import Logger


class S3Connector:
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

    def uploadImage(self, imageName):
        '''
        Upload a single image into the S3 bucket
        '''
        logger = Logger()
        self.s3Client.upload_file(
            f'{self.LocalImagePath}/{imageName}',
            self.S3ImageBucket,
            f'{self.S3ImageFolder}{imageName}'
        )
        logger.log(f'**Uploaded {imageName} to S3**')

    def deleteImage(self, imageName):
        '''
        Delete a single image from the S3 bucket
        '''
        logger = Logger()
        self.s3Resource.Object(
            self.S3ImageBucket, f'images/{imageName}'
            ).delete()
        logger.log(f'**Deleted {imageName} from S3**')
