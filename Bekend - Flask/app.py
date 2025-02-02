from flask import Flask, render_template, Blueprint, redirect, url_for, request, flash, session, make_response, jsonify
from config import Config
from extensions import db, login_manager, bcrypt
from flask_migrate import Migrate
from flask_login import login_user, logout_user, login_required, current_user
from controllers.user import add_user_function, edit_user_function, delete_user_function
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, unset_jwt_cookies, get_jwt
import sys
from models.user import User
from models.product import Product
from models.order import Order
import os
from utils import admin_required
from flask_cors import CORS, cross_origin
from werkzeug.security import check_password_hash


app = Flask(__name__)


CORS(app, supports_credentials=True, origins=["http://localhost:5173"], 
     resources={r"/*": {"origins": "http://localhost:5173"}}, 
     allow_headers=["Authorization", "Content-Type"])


app.config.from_object(Config)
app.secret_key = os.urandom(24)

db.init_app(app)
login_manager.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

migrate = Migrate(app, db)
########################## LOGIN LOGOUT ###########################
@app.route('/', methods=['POST'])
@cross_origin(origin='http://localhost:5173', supports_credentials=True)
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.get_by_email(email)

    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
        
        response = jsonify({"message": "Login successful!", "access_token": access_token})
        
        response.set_cookie(
            key='access_token_cookie',
            value=access_token,
            httponly=True,
            samesite="None",  
            secure=True  
        )

        return response, 200

    return jsonify({"message": "Invalid email or password"}), 401


@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"message": "Logged out successfully!"})
    unset_jwt_cookies(response)

    response.headers["Set-Cookie"] = "access_token_cookie=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT; HttpOnly; SameSite=None; Secure"

    return response, 200


########################## USER ###################################
@app.route('/users', methods=['GET'])
@jwt_required(locations=["cookies"])  
def get_users():
    current_user = get_jwt_identity()    
    users = User.get_all()
    return jsonify(users), 200



@app.route('/adduser', methods=['POST'])
@admin_required
def add_user():
    data = request.get_json()
    # Validacija podataka
    if not data or "username" not in data or "email" not in data or "password" not in data or "role" not in data:
        return jsonify({"message": "All fields are required"}), 400

    username = data["username"]
    email = data["email"]
    password = data["password"]
    role = data["role"]

    # Proveravamo da li korisnik već postoji
    existing_user = User.get_by_email(email)
    if existing_user:
        return jsonify({"message": "User with this email already exists"}), 409

    # Kreiranje i čuvanje korisnika
    new_user = User(username=username, email=email, role=role)
    new_user.set_password(password)  
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User added successfully!", "user": new_user.data}), 201

@app.route('/getuser/<int:id>', methods=['GET'])
def get_user(id):
    user = User.get_by_id(id)
    if not user:
        print("user not found")
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.data)


@app.route('/edituser/<int:id>', methods=['PUT'])
@admin_required
def edit_user(id):
    user = User.get_by_id(id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No data provided"}), 400

    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    if data.get("password"):  # Ako je prosleđen novi password, ažuriraj ga
        user.set_password(data["password"])
    user.role = data.get("role", user.role)

    db.session.commit()
    return jsonify({"message": "User updated successfully!", "user": user.data})

@app.route('/deleteuser/<int:id>', methods=['DELETE'])
@admin_required
def delete_user(id):
    user = User.get_by_id(id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Brisanje povezanih narudžbina pre brisanja korisnika
    orders = Order.query.filter_by(user_id=id).all()
    for order in orders:
        db.session.delete(order)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User successfully deleted!"})


########################## PRODUCT ###################################

@app.route('/products')
@cross_origin(origin='http://localhost:5173', supports_credentials=True)
def products():
    products = Product.get_all()
    return jsonify(products)

@app.route('/addproduct', methods=['GET', 'POST'])
def add_product():
    if request.method == "POST":
        data = request.get_json()  # Prima JSON podatke iz Vue-a
        if not data or "name" not in data or "description" not in data or "price" not in data:
            return jsonify({"error": "Invalid data"}), 400

        try:
            name = data["name"]
            description = data["description"]
            price = float(data["price"])

            product = Product(name=name, description=description, price=price)
            product.save()

            return jsonify({"message": "Product added successfully", "product": product.data}), 201
        except ValueError:
            return jsonify({"error": "Invalid price format"}), 400

    # GET zahtev vraćamo sve proizvode da ih Vue može prikazati ako je potrebno
    products = Product.query.all()
    products_data = [p.data for p in products]

    return jsonify(products_data)  


@app.route('/getproduct/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.get_by_id(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    return jsonify(product.data)


@app.route('/editproduct/<int:id>', methods=['PUT'])
def edit_product(id):
    product = Product.get_by_id(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = float(data.get("price", product.price))

    db.session.commit()
    return jsonify({"message": "Product updated successfully!", "product": product.data})


@app.route('/deleteproduct/<int:id>', methods=['DELETE'])
@admin_required
def delete_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    # Brisanje povezanih narudžbina
    orders = Order.query.filter_by(product_id=id).all()
    for order in orders:
        db.session.delete(order)

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product successfully deleted!"}), 200

########################## ORDER ###################################
@app.route('/orders')
def orders():
    all_orders = Order.query.all()
    orders_data = []

    for order in all_orders:
        user = User.query.get(order.user_id)  # Dohvati korisnika
        product = Product.query.get(order.product_id)  # Dohvati proizvod
        total_price = product.price * order.quantity  # Izračunaj cenu

        orders_data.append({
            "id": order.id,
            "customer": user.username if user else "Unknown",
            "total_price": total_price
        })

    return jsonify(orders_data) 


@app.route('/addorder', methods=['GET', 'POST'])
def add_order():
    if request.method == "POST":
        data = request.get_json()
        if not data or "user_id" not in data or "product_id" not in data or "quantity" not in data:
            return jsonify({"error": "Invalid data"}), 400

        try:
            user_id = int(data["user_id"])
            product_id = int(data["product_id"])
            quantity = int(data["quantity"])

            order = Order(user_id=user_id, product_id=product_id, quantity=quantity)
            db.session.add(order)
            db.session.commit()

            return jsonify({"message": "Order added successfully", "order": order.data}), 201
        except ValueError:
            return jsonify({"error": "Invalid data format"}), 400

    # GET metoda - vraća korisnike i proizvode da ih Vue može prikazati u dropdown listi
    users = User.query.all()
    products = Product.query.all()
    
    return jsonify({
        "users": [{"id": user.id, "name": user.username} for user in users],  
        "products": [{"id": product.id, "name": product.name} for product in products]
    })

@app.route('/getorder/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.get_by_id(id)
    if not order:
        return jsonify({"message": "Order not found"}), 404

    return jsonify({
        "id": order.id,
        "user_id": order.user_id,
        "product_id": order.product_id,
        "quantity": order.quantity
    })


@app.route('/editorder/<int:id>', methods=['PUT'])
def edit_order(id):
    order = Order.get_by_id(id)
    if not order:
        return jsonify({"message": "Order not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    order.user_id = int(data.get("user_id", order.user_id))
    order.product_id = int(data.get("product_id", order.product_id))
    order.quantity = int(data.get("quantity", order.quantity))

    db.session.commit()
    return jsonify({"message": "Order updated successfully!"})



@app.route('/deleteorder/<int:order_id>', methods=['DELETE'])
@admin_required
def delete_order(order_id):
    order = Order.query.get(order_id)  # Proveravamo da li order postoji

    if order is None:
        return jsonify({"message": "Order not found"}), 404  

    db.session.delete(order)
    db.session.commit()
    
    return jsonify({"message": "Order successfully deleted!"}), 200

app.run(debug=True)
