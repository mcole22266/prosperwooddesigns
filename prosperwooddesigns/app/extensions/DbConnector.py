from datetime import datetime

from .Logger import Logger

logger = Logger()


class DbConnector:

    def __init__(self):
        from app.models import db
        self.db = db

    def getAdmins(self):
        from app.models import Admin
        return Admin.query.all()

    def getAdmin(self, username=False, id=False):
        from app.models import Admin
        if username:
            return Admin.query.filter_by(username=username).first()
        if id:
            return Admin.query.filter_by(id=id).first()

    def setAdmin(self, username, password, firstname, lastname,
                 created_date=datetime.now(), commit=True):
        from app.models import Admin
        import flask_bcrypt

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
        from app.models import Request
        if order_id:
            # order by id desc
            return Request.query.order_by(Request.id.desc())
        else:
            return Request.query.all()

    def getRequest(self, id=False):
        from app.models import Request
        if id:
            return Request.query.filter_by(id=id).first()

    def setRequest(self, emailaddress, phonenumber, name, contactmethod,
                   description, how_hear, status='unread', is_archived=False,
                   created_date=datetime.now(),
                   commit=True):
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
        request = self.getRequest(id=id)

        self.db.session.delete(request)
        logger.log(f'Deleted Request - {request}')
        if commit:
            self.db.session.commit()

    def getImages(self):
        from app.models import Image
        return Image.query.all()

    def getImage(self, id=False):
        from app.models import Image
        if id:
            return Image.query.filter_by(id=id).first()

    def setImage(self, name, description, filename,
                 created_date=datetime.now(),
                 commit=True):
        from app.models import Image
        image = Image(name, description, filename, created_date)
        self.db.session.add(image)
        if commit:
            self.db.session.commit()
        logger.log(f'Created Image - {image}')
        return image

    def getLayouts(self):
        from app.models import Layout
        return Layout.query.all()

    def getLayout(self, id=False):
        from app.models import Layout
        if id:
            return Layout.query.filter_by(id=id).first()

    def setLayout(self, endpoint, content_name, content, is_image,
                  created_date, commit=True):
        from app.models import Layout
        layout = Layout(endpoint, content_name, content, is_image,
                        created_date=datetime.now())
        self.db.session.add(layout)
        if commit:
            self.db.session.commit()
        logger.log(f'Created Layout - {layout}')
        return layout

    def getContacts(self, order_id=False):
        from app.models import Contact
        if order_id:
            # order by id desc
            return Contact.query.order_by(Contact.id.desc())
        else:
            return Contact.query.all()

    def getContact(self, id=False):
        from app.models import Contact
        if id:
            return Contact.query.filter_by(id=id).first()

    def setContact(self, emailaddress, name, content, how_hear,
                   status='unread', is_archived=False,
                   created_date=datetime.now(),
                   commit=True):
        from app.models import Contact
        contact = Contact(emailaddress, name, content, how_hear, status,
                          is_archived, created_date)
        self.db.session.add(contact)
        if commit:
            self.db.session.commit()
        logger.log(f'Created Contact - {contact}')
        return contact

    def updateContact(self, id, status=False, is_archived=False,
                      commit=True):
        contact = self.getContact(id=id)
        if status:
            contact.status = status
            logger.log(
                f'Updated Contact {contact.id} status to {status}'
            )
        if is_archived:
            contact.is_archived = is_archived
            logger.log(
                f'Updated Contact {contact.id} - Now archived'
            )
        if commit:
            self.db.session.commit()

    def deleteContact(self, id, commit=True):
        contact = self.getContact(id=id)

        self.db.session.delete(contact)
        logger.log(f'Deleted Contact - {contact}')
        if commit:
            self.db.session.commit()
