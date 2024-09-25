from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from models import db, Product_details, User
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost3306/mysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '6f2a2a8a66ace64248fe489d6b734999'


db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username = data['usernmame']).first()
    if user and check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({"message": "Logged in successfully"})
    return jsonify({"message": "Invalid credentials"})
 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"})


@app.route('/admin/products', methods=['GET'])
@login_required
def admin_products():
    if current_user.role != 'admin':
        return jsonify({"message": "Unauthorized"})
 
    products = Product_details.query.all()
    products_list = [{"id": p.id, "name": p.p_name} for p in products]
    return jsonify(products_list)

@app.route('/user/products', methods=['GET'])
@login_required
def user_products():
    products = Product_details.query.all()
    products_list = [{"id": p.id, "name": p.p_name} for p in products]
    return jsonify(products_list)

@app.route('/create_user', methods = ['POST'])
def create_user():
    data = request.get_json()
    if User.query.filter_by(username = data['username']).first():
        return jsonify({" message": 'user already exixts'})
    hassed_passwords = generate_password_hash(data['password'] , methods = 'sha256')

    new_user = User(username = data['username'], password = hassed_passwords, role = data.get('role', 'user'))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'user created succesfully'})


@app.before_request
def create_tables():
    db.create_all()

@app.route('/add_product', methods=["POST"])
def add_product():
    if current_user.role != 'admin':
        return jsonify({"message": "unauthorized user"})
    
    data = request.get_json()

    if isinstance(data, list):
        added_products = []
        for p_data in data:
            p_name = p_data.get("p_name")
            p_price = p_data.get("p_price")
            p_category = p_data.get("p_category")
            p_stock = p_data.get('p_stock')
            p_description = p_data.get("p_description")
            p_img = p_data.get('p_img')

            new_product = Product_details(p_name = p_name, p_price = p_price, p_category = p_category, p_stock = p_stock, p_description = p_description, p_img = p_img)
            db.session.add(new_product)
            db.session.commit()

            added_products.append({'p_name' : p_name,
            'p_price' : p_price,
            'p_category' : p_category,
            'p_stock' : p_stock,
            'p_description' : p_description,
            'p_img' : p_img
            })

        return jsonify({
            'message': 'added successfully',
            'product': added_products})
    else:
        return jsonify({'message': 'invalid input , expected list'})
    

@app.route('/products', methods = ['GET'])
def get_products():
    products = Product_details.query.all()
    product_list = []

    for product in products:
        product_list.append({
            "id": product.id,
            "p_name" : product.p_name,
            "p_price" : product.p_price,
            "p_category" : product.p_category,
            "p_stock" : product.p_stock,
            "p_description" : product.p_description,
            "p_img" : product.p_img,
        })
    return jsonify({"products":product_list})

@app.route('/products/<int:id>', methods = ['GET'])
def get_product(id):
    product =Product_details.query.get(id)
    if product:
        return jsonify({
            "id": product.id,
            "p_name" : product.p_name,
            "p_price" : product.p_price,
            "p_category" : product.p_category,
            "p_stock" : product.p_stock,
            "p_description" : product.p_description,
            "p_img" : product.p_img,
        })
    else:
        return jsonify({"message": 'product not found'})
    
@app.route('/update_products/<int:id>', methods = ['PUT'])   
def update_product(id):
    if current_user.role != 'admin':
        return jsonify({"message": 'unauthorized user'})
    
    product = Product_details.query.get(id)
    if product:
        data = request.get_json()
        product.p_name = data.get('p_name', product.p_name)
        product.p_price = data.get('p_price', product.p_price)
        product.p_stock = data.get('p_stock', product.p_stock)
        product.p_category = data.get('p_category', product.p_category)
        product.p_description = data.get('p_description', product.p_description)
        product.p_img = data.get('p_img', product.p_img)

        db.session.commit()
        return jsonify({"message":'updated Successfully'})
    else:
        return jsonify({"message":'product not found'})
    

@app.route('/delete_products/<int:id>/', methods = ['DELETE'])
def delete(id):
    if current_user.role != 'admin':
        return jsonify({"message": 'unauthorized user'})
    
    product = Product_details.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message':'product delete successfully '})


if __name__=='__main___':
    app.run(debug=True)

