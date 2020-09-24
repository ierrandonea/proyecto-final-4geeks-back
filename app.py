import json, os, datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from models import db, User, Product, Category, ProductCategory
from config import Development

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(Development)

db.init_app(app)
jwt = JWTManager(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
CORS(app)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/api/login", methods=['POST'])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)    

    if not email:
        return jsonify({"msg": {"email": "Email is required"}}), 400
    
    if not password:
        return jsonify({"msg": {"password": "Password is required"}}), 400

    user = User.query.filter_by(email = email).first()

    if not user:
        return jsonify({"msg": {"not_user": "Email/password is incorrect"}}), 401

    if not check_password_hash(user.password, password):
        return jsonify({"msg": {"not_password": "Email/password is incorrect"}}), 401
    
    expire_in = datetime.timedelta(days = 3)
    data = {
        "access_token": create_access_token(identity=user.id, expires_delta = expire_in),
        "user": user.serialize()
    }

    return jsonify(data), 200

@app.route("/api/register", methods=['POST'])
def register():
    name = request.json.get("name", None)
    last_name = request.json.get("last_name", None)
    password = request.json.get("password", None)
    email = request.json.get("email", None)   
    phone = request.json.get("phone", None)
    address = request.json.get("address", None)

    if not name:
        return jsonify({"msg": "Name is required"}), 400
    
    if not last_name:
        return jsonify({"msg": "Last name is required"}), 400
    
    if not password:
        return jsonify({"msg": "Password is required"}), 400

    if not email:
        return jsonify({"msg": "Email is required"}), 400  
    
    if not phone:
        return jsonify({"msg": "Phone is required"}), 400
    
    if not address:
        return jsonify({"msg": "Address is required"}), 400
    
    user = User.query.filter_by(email = email).first()
    print(user)

    if user:
        return jsonify({"msg": "User already exists"}), 400

    user = User()
    user.name = name
    user.last_name = last_name
    user.password = generate_password_hash(password)
    user.email = email    
    user.phone = phone
    user.address = address
    user.save()

    expire_in = datetime.timedelta(days = 3)
    data = {
        "access_token": create_access_token(identity=user.id, expires_delta = expire_in),
        "user": user.serialize()
    }

    return jsonify(data), 200

@app.route("/api/profile")
@jwt_required
def profile():

    id = get_jwt_identity()
    user = User.query.get(id)
    return jsonify(user.serialize()), 200 

# @app.route("/api/users", methods=['GET', 'POST', 'PUT', 'DELETE'])

@app.route("/api/categories/", methods=['GET', 'POST'])
@app.route("/api/categories/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def categories(id = None):
    if request.method == 'GET':
        if id is not None:
            category = Category.query.get(id)
            if category:
                return jsonify(category.serialize()), 200
            else:
                return jsonify({"msg": "Category not found"}), 404
        else:
            categories = Category.query.all()
            categories = list(map(lambda category: category.serialize(), categories))
            return jsonify(categories), 200
    if request.method == 'POST':
        name = request.json.get("name", None)
        if not name:
            return jsonify({"msg": "name is missing"}), 400
        else:
            category = Category()
            category.name = name
            category.save()
            return jsonify(category.serialize()), 201
    if request.method == 'PUT':
        if not id:
            return jsonify({"msg": "product not found"}), 404
        else:
            name = request.json.get("name", None)  
            if not name:
                return jsonify({"msg": "name is missing"}), 400
            else:                                
                category = Category.query.get(id)
                category.update()
                return jsonify(category.serialize()), 200
    if request.method == 'DELETE':
        category = Category.query.get(id)
        if not category:
            return jsonify({"msg": "Category not found"}), 404
        category.delete()
        return jsonify({"msg": "Category succesfully deleted"}), 200


@app.route("/api/products/order/<sorting>", methods=['GET'])        
@app.route("/api/products/", methods=['GET', 'POST'])
@app.route("/api/products/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def products(id = None, sorting = None):
    if request.method == 'GET':
        if sorting is not None:
            if sorting == 'priceup':
                products = Product.query.order_by(Product.price.asc()).all()
                products = list(map(lambda product: product.serialize_w_categories(), products))
                return jsonify(products), 200
            elif sorting == 'pricedown':
                products = Product.query.order_by(Product.price.desc()).all()
                products = list(map(lambda product: product.serialize_w_categories(), products))
                return jsonify(products), 200
            elif sorting == 'brandup':
                products = Product.query.order_by(Product.brand.asc()).all()
                products = list(map(lambda product: product.serialize_w_categories(), products))
                return jsonify(products), 200
            elif sorting == 'branddown':
                products = Product.query.order_by(Product.brand.desc()).all()
                products = list(map(lambda product: product.serialize_w_categories(), products))
                return jsonify(products), 200
        elif id is not None:
            products = Product.query.get(id)
            if products:
                return jsonify(products.serialize_w_categories()), 200
            else:
                return jsonify({"msg": "product not found"}), 404
        else:
            products = Product.query.all()
            products = list(map(lambda product: product.serialize_w_categories(), products))
            return jsonify(products), 200
    if request.method == 'POST':
        sku = request.json.get("sku", None)
        brand = request.json.get("brand", None)
        name = request.json.get("name", None)
        presentation = request.json.get("presentation", None)
        price = request.json.get("price", None)
        stock = request.json.get("stock", None)
        origin = request.json.get("origin", None)
        species = request.json.get("species", None)
        ground = request.json.get("ground", None)
        acidity = request.json.get("acidity", None)
        roasting = request.json.get("roasting", None)
        description = request.json.get("description", None)
        image = request.json.get("image", None)
        categories = request.json.get("categories", None)      
        if not sku and price and brand and name and presentation and attributes and description:
            return jsonify({"msg": "some fields are missing"}), 400
        else:
            product = Product()
            product.sku = sku
            product.brand = brand
            product.name = name
            product.price = price
            product.stock = stock
            product.origin = origin
            product.species = species
            product.ground = ground
            product.acidity = acidity
            product.roasting = roasting
            product.presentation = presentation
            product.description = description
            product.image = image
            for category in categories:
                p_cat = Category.query.get(category)
                p_cat.category_id = category
                product.categories.append(p_cat)
            product.save()
            return jsonify(product.serialize_w_categories()), 201
    if request.method == 'PUT':
        if not id:
            return jsonify({"msg": "product not found"}), 404
        else:
            sku = request.json.get("sku", None)
            brand = request.json.get("brand", None)
            name = request.json.get("name", None)
            presentation = request.json.get("presentation", None)
            price = request.json.get("price", None)
            stock = request.json.get("stock", None)
            origin = request.json.get("origin", None)
            species = request.json.get("species", None)
            ground = request.json.get("ground", None)
            acidity = request.json.get("acidity", None)
            roasting = request.json.get("roasting", None)
            description = request.json.get("description", None)
            image = request.json.get("image", None) 
            # if not sku or price or brand or name or presentation or attributes or description or stock:
            if not sku:
                return jsonify({"msg": "some fields are missing"}), 400
            else:                                
                product = Product.query.get(id)
                product.sku = sku
                product.brand = brand
                product.name = name
                product.price = price
                product.stock = stock
                product.origin = origin
                product.species = species
                product.ground = ground
                product.acidity = acidity
                product.roasting = roasting
                product.presentation = presentation
                product.description = description
                product.image = image
                product.update()
                return jsonify(product.serialize()), 200
    if request.method == 'DELETE':
        product = Product.query.get(id)
        if not product:
            return jsonify({"msg": "Product not found"}), 404
        product.delete()
        return jsonify({"msg": "Product succesfully deleted"}), 200
# @app.route("/api/content", methods=['GET', 'POST', 'PUT', 'DELETE'])
# @app.route("/api/events", methods=['GET', 'POST', 'PUT', 'DELETE'])
if __name__ == "__main__":
    manager.run()