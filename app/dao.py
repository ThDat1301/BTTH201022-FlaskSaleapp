import json
from app import app


def load_categories():
    with open(f'{app.root_path}/data/categories.json', "r", encoding="utf-8") as f:
        return json.load(f)


def load_products(category_id=None, kw=None, from_price=None, to_price=None):
    with open(f'{app.root_path}/data/products.json', "r", encoding="utf-8") as f:
        products = json.load(f)

    if category_id:
        products = [p for p in products if p['category_id'] == int(category_id)]
    if kw:
        products = [p for p in products if p['name'].lower().find(kw.lower()) >= 0]
    if from_price:
        products = [p for p in products if p['price'] >= float(from_price)]
    if to_price:
        products = [p for p in products if p['price'] <= float(to_price)]
    return products


def get_product_by_id(product_id):
    with open(f'{app.root_path}/data/products.json', "r", encoding="utf-8") as f:
        products = json.load(f)

    for product in products:
        if product['id'] == product_id:
            return product