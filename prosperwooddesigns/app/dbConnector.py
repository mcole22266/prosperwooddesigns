class AdminConnector:

    def get(self):
        from .models import Admin
        admins = Admin.query.all()
        return admins
