# MockData.py
# Michael Cole
#
# Generates MockData for the app -- especially in development mode
# -----------------------------------------------------------------

import os
from datetime import datetime

from .DbConnector import DbConnector
from .Logger import Logger


class MockData:
    '''
    Loads database with mock data for developing and testing
    '''
    from faker import Faker

    # Instantiate variables
    fake = Faker()
    dbConn = DbConnector()
    logger = Logger()

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
        '''
        Generates a fake description
        '''
        description = ''
        paragraphs = self.fake.paragraphs(self.fake.random_int(
            num_paragraphs_min, num_paragraphs_max
            )
        )
        for paragraph in paragraphs:
            description += f'{paragraph} '
        description = description[:-1]  # account for extra space
        return description

    def hasData(self, db):
        '''
        Check if database is empty
        '''

        # Get a few tables from the database
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
            # fake some data
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
            # fake some data
            emailaddress = self.fake.email()
            phonenumber = self.fake.phone_number()
            name = self.fake.name()
            contactmethod = self.fake.random_element([
                'phone', 'email', None
            ])
            description = self.fakeDescription()
            how_hear = self.fake.random_element([
                'Facebook', 'Instagram', 'Ad', 'Word of Mouth'
            ])
            status = self.fake.random_element([
                'unread', 'read', 'in progress', 'ready to deliver', 'complete'
            ])
            is_archived = self.fake.boolean(chance_of_getting_true=20)
            created_date = self.fakeDate()

            self.dbConn.setRequest(emailaddress, phonenumber, name,
                                   contactmethod, description, how_hear,
                                   status, is_archived, created_date,
                                   commit=False)
        db.session.commit()

    def loadImage(self, db, num_rows=20):
        '''
        Load Image table with fake data
        '''

        for i in range(num_rows):
            # fake some data
            location = self.fake.file_path()
            product_id = self.fake.random_int(1, 15)
            created_date = self.fakeDate()

            self.dbConn.setImage(location, product_id,
                                 created_date, commit=False)
        db.session.commit()

    def loadProduct(self, db, num_rows=15):
        '''
        Load Product table with fake data
        '''

        for i in range(num_rows):
            # fake some data
            name = self.fake.word()
            description = self.fakeDescription(2, 3)
            created_date = self.fakeDate()

            self.dbConn.setProduct(name, description, created_date,
                                   commit=False)

        db.session.commit()

    def loadLayout(self, db, num_rows=30):
        '''
        Load Layout table with fake data
        '''

        for i in range(num_rows):
            # fake some data
            endpoint = self.fake.uri_path()
            content_name = self.fake.word()
            content = self.fakeDescription(2, 3)
            is_image = self.fake.boolean()
            created_date = self.fakeDate()

            self.dbConn.setLayout(endpoint, content_name, content,
                                  is_image, created_date,
                                  commit=False)
        db.session.commit()

    def loadQuestion(self, db, num_rows=20):
        '''
        Load Question table with fake data
        '''

        for i in range(num_rows):
            # fake some data
            emailaddress = self.fake.email()
            name = self.fake.name()
            content = self.fakeDescription()
            how_hear = self.fake.random_element([
                'Facebook', 'Instagram', 'Ad', 'Word of Mouth'
            ])
            status = self.fake.random_element([
                'unread', 'read',
            ])
            created_date = self.fakeDate()
            is_archived = self.fake.boolean(chance_of_getting_true=20)

            self.dbConn.setQuestion(emailaddress, name, content, how_hear,
                                    status, is_archived, created_date,
                                    commit=False)
        db.session.commit()

    def loadContact(self, db, num_rows=20):
        '''
        Load Contact table with fake data
        '''

        for i in range(num_rows):
            # fake some data
            name = self.fake.name()
            phonenumber = self.fake.phone_number()
            emailaddress = self.fake.email()

            self.dbConn.setContact(name, phonenumber, emailaddress)

        db.session.commit()

    def loadJoined_ProductImage(self, db):
        '''
        Load Product and Image tables with hard-coded "real" data
        '''

        imageDir = '/prosperwooddesigns/app/static/images'
        relimageDir = '../static/images'
        for filename in os.listdir(imageDir):
            path = f'{relimageDir}/{filename}'
            if 'cornhole_football' in filename:
                if '00' in filename:
                    featured = True
                else:
                    featured = False
                self.dbConn.setJoined_ProductImage(
                    'Cornhole Football Board',
                    'This is the description for a football cornhole board',
                    path,
                    is_featured_img=featured,
                    is_featured_product=True
                    )
            elif 'cornhole' in filename:
                self.dbConn.setJoined_ProductImage(
                    'Cornhole Board',
                    'This is the description for a cornhole board',
                    path,
                    is_featured_img=True
                )
            elif 'cabinet' in filename:
                self.dbConn.setJoined_ProductImage(
                    'Custom Cabinet',
                    'This is the description for a custom cabinet',
                    path,
                    is_featured_img=True,
                    is_featured_product=True
                )
            elif 'exercise' in filename:
                self.dbConn.setJoined_ProductImage(
                    'Exercise Box',
                    'This is the description for an exercise box',
                    path,
                    is_featured_img=True
                )
            elif 'decor_holiday' in filename:
                if '00' in filename:
                    featured = True
                else:
                    featured = False
                self.dbConn.setJoined_ProductImage(
                    'Customized Holiday Decor Board',
                    'This is the description for a custom holiday decorative \
                        board',
                    path,
                    is_featured_img=featured,
                    is_featured_product=True
                )
            elif 'decor_name' in filename:
                if '00' in filename:
                    featured = True
                else:
                    featured = False
                self.dbConn.setJoined_ProductImage(
                    'Customized Name Decor Board',
                    'This is the description for a custom name decorative \
                        board',
                    path,
                    is_featured_img=featured
                )
            elif 'decor' in filename:
                self.dbConn.setJoined_ProductImage(
                    'Customized Decor Board',
                    'This is the description for a custom decor board',
                    path,
                    is_featured_img=True
                )
