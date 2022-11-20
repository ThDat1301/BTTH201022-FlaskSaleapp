from app import app, db
from flask_admin import Admin
from app.models import Category, Product, UserRole
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask_admin import BaseView, expose
from flask import redirect

admin = Admin(app=app, name="E-Commerce Administration", template_mode='bootstrap4')


class ProductView(ModelView):
    can_view_details = True
    can_export = True
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(AuthenticatedModelView(Category, db.session))
admin.add_view(AuthenticatedModelView(Product, db.session))
admin.add_view(LogoutView(name='Logout'))
