import json
from app import app, db
from app.models import Category, Product, User, UserRole, Receipt, ReceiptDetail
import hashlib
from flask_login import current_user


def load_categories():
    # with open(f'{app.root_path}/data/categories.json', "r", encoding="utf-8") as f:
    #     return json.load(f)
    return Category.query.all()


def load_products(category_id=None, kw=None, from_price=None, to_price=None, page=1):
    # with open(f'{app.root_path}/data/products.json', "r", encoding="utf-8") as f:
    #     products = json.load(f)
    #
    # if category_id:
    #     products = [p for p in products if p['category_id'] == int(category_id)]
    # if kw:
    #     products = [p for p in products if p['name'].lower().find(kw.lower()) >= 0]
    # if from_price:
    #     products = [p for p in products if p['price'] >= float(from_price)]
    # if to_price:
    #     products = [p for p in products if p['price'] <= float(to_price)]
    # return products
    products = Product.query.filter(Product.active.__eq__(True))
    if category_id:
        products = products.filter(Product.category_id.__eq__(category_id))
    if kw:
        products = products.filter(Product.name.contains(kw))
    if from_price:
        products = products.filter(Product.price.__ge__(from_price))
    if to_price:
        products = products.filter(Product.price.__le__(to_price))
    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size
    return products.slice(start, end).all()


def get_product_by_id(product_id):
    # with open(f'{app.root_path}/data/products.json', "r", encoding="utf-8") as f:
    #     products = json.load(f)
    #
    # for product in products:
    #     if product['id'] == product_id:
    #         return product
    return Product.query.get(product_id)


def add_receipt(cart):
    if cart:
        receipt = Receipt(user=current_user)
        db.session.add(receipt)
        for c in cart.values():
            d = ReceiptDetail(receipt=receipt,
                              product_id=c['id'],
                              quantity=c['quantity'],
                              unit_price=c['price'])
            db.session.add(d)
        db.session.commit()

def count_product():
    return Product.query.filter(Product.active.__eq__(True)).count()


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name,
                username=username,
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))
    db.session.add(user)
    db.session.commit()


def check_login(username, password, role=UserRole.USER):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 ).first()


def count_cart(cart):
    total_quantity, total_ammount = 0, 0
    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_ammount += c['quantity'] * c['price']
    return {
        'total_quantity': total_quantity,
        'total_ammount': total_ammount
    }

def get_user_by_id(user_id):
    return User.query.get(user_id)