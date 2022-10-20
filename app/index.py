from app import app, dao
from flask import render_template, request


@app.route("/")
def home():
    categories = dao.load_categories()
    products = dao.load_products(category_id=request.args.get("category_id"))
    return render_template("index.html", categories=categories, products=products)


if __name__ == '__main__':
    app.run(debug=True)