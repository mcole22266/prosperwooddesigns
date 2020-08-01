# extensions.py
# Michael Cole

# Collection of extensions to be used throughout the app
# ------------------------------------------------------

import sys
import os
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
        self.LocalImagePath = '/prosperwooddesigns/app/static/images'
        self.S3ImageBucket = 'prosperwooddesigns'
        self.S3ImageFolder = 'images/'

        # connect to S3
        self.s3Client = boto3.client('s3')
        self.s3Resource = boto3.resource('s3')

    def uploadImages(self):
        '''
        Uploads all images in the images directory of this project
        '''
        self.images = [f for f in os.listdir(self.LocalImagePath)]
        for imageName in self.images:
            self.s3Client.upload_file(
                f'{self.LocalImagePath}/{imageName}',  # local image name
                self.S3ImageBucket,  # bucket name
                f'{self.S3ImageFolder}{imageName}')  # remote image name

    def downloadImages(self):
        '''
        Downloads all images from the S3 bucket into the images directory
        of this project
        '''
        bucket = self.s3Resource.Bucket(self.S3ImageBucket)
        objects = bucket.objects.filter(Prefix=self.S3ImageFolder)
        for obj in objects:
            path, filename = os.path.split(obj.key)
            if filename != '':
                bucket.download_file(
                    obj.key,
                    f'{self.LocalImagePath}/{filename}')
