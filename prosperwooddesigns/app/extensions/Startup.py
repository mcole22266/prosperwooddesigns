# Startup.py
# Michael Cole
#
# Startup is used for all operations upon app startup
# ---------------------------------------------------

import os

from app.extensions.DbConnector import DbConnector


class Startup:

    def __init__(self):
        self.dbConn = DbConnector()
        self.featured_products = []

    def hasData(self, db):
        '''
        Check if particular tables are empty
        '''

        # Get a few tables from the database
        products = self.dbConn.getProducts()
        images = self.dbConn.getImages()

        if len(products) > 3 or len(images) > 3:
            return True
        return False

    def loadInitialData(self):
        '''
        Load all initial data needed for the app such as initial product
        data and layout data
        '''

        # layout
        # index page
        self.dbConn.setLayout(
            'Index Page',
            'Cover Tag Line',
            'Your one-stop-shop for your custom wood designs!'
        )
        self.dbConn.setLayout(
            'Index Page',
            'Featured Header',
            'Featured Designs'
        )
        self.dbConn.setLayout(
            'Index Page',
            'Featured Buttons',
            'Check it out!'
        )
        self.dbConn.setLayout(
            'Index Page',
            'Designs Page Alert Header',
            'Check out the rest of our designs!'
        )
        self.dbConn.setLayout(
            'Index Page',
            'Designs Page Alert Button',
            'Show me more!'
        )
        # Contact Card
        self.dbConn.setLayout(
            'Contact Card',
            'Name',
            'John Manning'
        )
        self.dbConn.setLayout(
            'Contact Card',
            'Phone',
            '856-577-4087'
        )
        self.dbConn.setLayout(
            'Contact Card',
            'Email',
            'prosperwooddesigns@gmail.com'
        )
        self.dbConn.setLayout(
            'Contact Card',
            'Button',
            'Ask a Question'
        )
        # Designs Page
        self.dbConn.setLayout(
            'Designs Page',
            'Header',
            'Check out some of our designs!'
        )
        self.dbConn.setLayout(
            'Designs Page',
            'Buttons',
            'See More'
        )

        # products
        # cornhole football board
        cornhole_football_name = 'Cornhole Football Board'
        self.featured_products.append(cornhole_football_name)
        cornhole_football_image = 'cornhole_football00.jpeg'
        cornhole_football_description = '''
### First to throw for 100 yards wins!

Customize them for your favorite NFL, College, or High School Team and be the envy
of the neighborhood.

Oh, and check out the "Beverage" holders at the top of the goal posts. No more
spilling your drink on the lawn while you're throwing the winning shot!
'''
        # cornhole board
        cornhole_name = 'Cornhole Board'
        cornhole_image = 'cornhole00.jpeg'
        cornhole_description = '''
Just tell me what you'd like on-em if you already have a design in mind.
'''
        # cabinet
        cabinet_name = 'Custom Cabinet'
        self.featured_products.append(cabinet_name)
        cabinet_image = 'cabinet00.jpeg'
        cabinet_description = '''
Display what you'd like and hide the rest in this stunning cabinet!
Goes perfectly in the bathroom or even in the kitchen. Or, hang one
in your family room as a beautiful decorative
and functional piece.
'''
        # exercise box
        exercise_box_name = 'Exercise Box'
        exercise_box_image = 'exercisebox00.jpeg'
        exercise_box_description = '''
No home gym is complete without the complete workout tool available today!
Sit up, push up, jump up, and **step up your game** with
this amazing workout tool.

It comes in 4 sizes _(Width x Height x Depth)_:

- Small - 16x14x12
- Medium - 20x18x16
- Large - 24x20x16
- X-Large - 30x24x20
'''
        # holiday decor
        holiday_decor_name = 'Customized Holiday Decor Board'
        holidary_decor_image = 'decor_holiday00.jpeg'
        holiday_decor_description = '''
These can be made to fit your size needs and customized in any way you'd like with or without handles

- Holidays
- Memoralize a Special Event
- Show off your team, town, or ISD spirit
- You dream it and I'll build it!
'''
        # name decor
        name_decor_name = 'Customized Name Decor Board'
        name_decor_image = 'decor_name00.jpeg'
        name_decor_description = '''
These can be made to fit your size needs and customized in any way you'd like with or without handles

- Holidays
- Memoralize a Special Event
- Show off your team, town, or ISD spirit
- You dream it and I'll build it!
'''
        # decor
        decor_name = 'Customized Decor Board'
        decor_image = 'decor_board00.jpeg'
        decor_description = '''
These can be made to fit your size needs and customized in any way you'd like with or without handles

- Holidays
- Memoralize a Special Event
- Show off your team, town, or ISD spirit
- You dream it and I'll build it!
'''
        imageDir = '/prosperwooddesigns/app/static/images'
        relimageDir = '../static/images'
        for filename in os.listdir(imageDir):
            path = f'{relimageDir}/{filename}'
            if 'cornhole_football' in filename:
                if filename == cornhole_football_image:
                    featured = True
                else:
                    featured = False
                self.dbConn.setJoined_ProductImage(
                    cornhole_football_name,
                    cornhole_football_description,
                    path,
                    is_featured_img=featured,
                    is_featured_product=True
                    )
            elif 'cornhole' in filename:
                if filename == cornhole_image:
                    featured = True
                else:
                    featured = False
                self.dbConn.setJoined_ProductImage(
                    cornhole_name,
                    cornhole_description,
                    path,
                    is_featured_img=featured
                )
            elif 'cabinet' in filename:
                if filename == cabinet_image:
                    featured = True
                else:
                    featured = False
                self.dbConn.setJoined_ProductImage(
                    cabinet_name,
                    cabinet_description,
                    path,
                    is_featured_img=featured,
                    is_featured_product=True
                )
            elif 'exercise' in filename:
                if filename == exercise_box_image:
                    featured = True
                else:
                    featured = False
                self.dbConn.setJoined_ProductImage(
                    exercise_box_name,
                    exercise_box_description,
                    path,
                    is_featured_img=featured
                )
            elif 'decor_holiday' in filename:
                if filename == holidary_decor_image:
                    featured = True
                else:
                    featured = False
                self.dbConn.setJoined_ProductImage(
                    holiday_decor_name,
                    holiday_decor_description,
                    path,
                    is_featured_img=featured,
                    is_featured_product=True
                )
            elif 'decor_name' in filename:
                if filename == name_decor_image:
                    featured = True
                else:
                    featured = False
                self.dbConn.setJoined_ProductImage(
                    name_decor_name,
                    name_decor_description,
                    path,
                    is_featured_img=featured
                )
            elif 'decor' in filename:
                if filename == decor_image:
                    featured = True
                else:
                    featured = False
                self.dbConn.setJoined_ProductImage(
                    decor_name,
                    decor_description,
                    path,
                    is_featured_img=featured
                )
