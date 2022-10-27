from app import app, dao
from flask import render_template, request


@app.route("/")
def home():
    categories = dao.load_categories()
    products = dao.load_products(category_id=request.args.get("category_id"),
                                 kw=request.args.get("keyword"),
                                 from_price=request.args.get("from_price"),
                                 to_price=request.args.get("to_price"))
    return render_template("index.html", categories=categories, products=products)


@app.route("/<int:product_id>")
def product_detail(product_id):
    product = dao.get_product_by_id(product_id)
    return render_template("product_detail.html", product=product)


if __name__ == '__main__':
    app.run(debug=True)