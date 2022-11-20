import math
import cloudinary.uploader
from app import app, dao, login
from flask import render_template, request, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, login_required
from app.models import UserRole


@app.route("/")
def home():
    products = dao.load_products(category_id=request.args.get("category_id"),
                                 kw=request.args.get("keyword"),
                                 from_price=request.args.get("from_price"),
                                 to_price=request.args.get("to_price"),
                                 page=int(request.args.get('page', 1)))
    counter = dao.count_product()
    return render_template("layout/index.html", products=products,
                           pages=math.ceil(counter/app.config['PAGE_SIZE']))


@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = dao.get_product_by_id(product_id)
    return render_template("layout/product_detail.html", product=product)


@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        email = request.form.get('email')
        avt_path = None
        try:
            if password.strip().__eq__(password_confirm.strip()):

                avatar = request.files.get('avt')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avt_path = res['secure_url']

                dao.add_user(name=name,
                             username=username,
                             password=password,
                             email=email,
                             avatar=avt_path)
                return redirect(url_for('user_signin'))
            else:
                err_msg = "Mật khẩu không khớp!"

        except Exception as ex:
            err_msg = 'Hệ thống đang có lỗi: ' + str(ex)

    return render_template('register.html', err_msg=err_msg)


@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            next = request.args.get('next', 'home')
            return redirect(url_for(next))
        else:
            err_msg = "Username hoặc mật khẩu không chính xác!"
    return render_template('login.html', err_msg=err_msg)


@app.route('/admin-login', methods=['post'])
def admin_signin():

    username = request.form['username']
    password = request.form['password']

    user = dao.check_login(username=username,
                           password=password,
                           role=UserRole.ADMIN)
    if user:
        login_user(user=user)

        return redirect('/admin')

    else:
        return redirect('/admin')


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('home'))


@app.context_processor
def common_response():
    return {
        'categories': dao.load_categories(),
        'cart_stats': dao.count_cart(session.get('cart'))
    }


@login.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/api/add-cart', methods=['post'])
def add_to_cart():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')

    cart = session.get('cart')
    if not cart:
        cart = {}

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': 1
        }
    session['cart'] = cart
    return jsonify(dao.count_cart(cart))


@app.route('/cart')
@login_required
def cart():
    return render_template('cart.html',
                           stats=dao.count_cart(session.get('cart')))


@app.route('/api/pay', methods=['post'])
@login_required
def pay():
    try:
        dao.add_receipt(session.get('cart'))
        del session['cart']
    except:
        return jsonify({'code': 400})
    return jsonify({'code': 200})


if __name__ == '__main__':
    from app.admin import *
    app.run(debug=True)