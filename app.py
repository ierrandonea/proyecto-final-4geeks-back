import json
import os
import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from models import db, User, Product, Category, ProductCategory, Content
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

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"msg": {"not_user": "Email/password is incorrect"}}), 401

    if not check_password_hash(user.password, password):
        return jsonify({"msg": {"not_password": "Email/password is incorrect"}}), 401

    expire_in = datetime.timedelta(days=3)
    data = {
        "access_token": create_access_token(identity=user.id, expires_delta=expire_in),
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

    user = User.query.filter_by(email=email).first()
    print(user)

    if user:
        return jsonify({"msg": {"reg_not_user": "User already exists"}}), 400

    user = User()
    user.name = name
    user.last_name = last_name
    user.password = generate_password_hash(password)
    user.email = email
    user.phone = phone
    user.address = address
    user.save()

    expire_in = datetime.timedelta(days=3)
    data = {
        "access_token": create_access_token(identity=user.id, expires_delta=expire_in),
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
def categories(id=None):
    if request.method == 'GET':
        if id is not None:
            category = Category.query.get(id)
            if category:
                return jsonify(category.serialize()), 200
            else:
                return jsonify({"msg": "Category not found"}), 404
        else:
            categories = Category.query.all()
            categories = list(
                map(lambda category: category.serialize(), categories))
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


@app.route("/api/products/", methods=['GET', 'POST'])
@app.route("/api/products/brewing", methods=['POST'])
@app.route("/api/products/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def products(id=None):
    if request.method == 'GET':
        if id is not None:
            products = Product.query.get(id)
            if products:
                return jsonify(products.serialize_w_categories()), 200
            else:
                return jsonify({"msg": "product not found"}), 404
        else:
            products = Product.query.all()
            products = list(
                map(lambda product: product.serialize_w_categories(), products))
            return jsonify(products), 200
    if request.method == 'POST':
        # the parameters below are to get products filtered
        sorting = request.json.get("sorting", None)
        groundFilter = request.json.get("groundFilter", None)
        originFilter = request.json.get("originFilter", None)
        pricefilterMin = request.json.get("pricefilterMin", None)
        pricefilterMax = request.json.get("pricefilterMax", None)
        # the parameter below are for registering a new product
        sku= request.json.get("sku", None)
        brand= request.json.get("brand", None)
        name= request.json.get("name", None)
        presentation= request.json.get("presentation", None)
        price= request.json.get("price", None)
        stock= request.json.get("stock", None)
        origin= request.json.get("origin", None)
        species= request.json.get("species", None)
        ground= request.json.get("ground", None)
        acidity= request.json.get("acidity", None)
        roasting= request.json.get("roasting", None)
        description= request.json.get("description", None)
        image= request.json.get("image", None)
        categories= request.json.get("categories", None)
        # all below validates for the filters, I know it's not the prettiest code in the world, but it works ;)
        if not groundFilter and originFilter:
            if sorting == 'priceup':
                products = Product.query.filter(Product.origin.in_((originFilter)), Product.price.between(pricefilterMin, pricefilterMax)).order_by(Product.price.asc()).all()
                products = products
                products = list(map(lambda product: product.serialize_w_categories(), products))
                return jsonify(products), 200
            elif sorting == 'pricedown':
                products = Product.query.filter(Product.origin.in_((originFilter)), Product.price.between(pricefilterMin, pricefilterMax)).order_by(Product.price.desc()).all()
                products = list(map(lambda product: product.serialize_w_categories(), products))
                return jsonify(products), 200
            elif sorting == 'brandup':
                products = Product.query.filter(Product.origin.in_((originFilter)), Product.price.between(pricefilterMin, pricefilterMax)).order_by(Product.brand.asc()).all()
                products = list(map(lambda product: product.serialize_w_categories(), products))
                return jsonify(products), 200
            elif sorting == 'branddown':
                products = Product.query.filter(Product.origin.in_((originFilter)), Product.price.between(pricefilterMin, pricefilterMax)).order_by(Product.brand.desc()).all()
                products = list(map(lambda product: product.serialize_w_categories(), products))
                return jsonify(products), 200                  
        elif not originFilter and groundFilter:
            if sorting == 'priceup':
                products = Product.query.filter(Product.ground.in_((groundFilter)), Product.price.between(pricefilterMin, pricefilterMax)).order_by(Product.price.asc()).all()
                products = list(map(lambda product: product.serialize_w_categories(), products))
                return jsonify(products), 200
            elif sorting == 'pricedown':
                products = Product.query.filter(Product.ground.in_((groundFilter)), Product.price.between(pricefilterMin, pricefilterMax)).order_by(Product.price.desc()).all()
                products = list(map(lambda product: product.serialize_w_categories(), products))
                return jsonify(products), 200
            elif sorting == 'brandup':
                products = list(map(lambda product: product.serialize_w_categories(), products))
                return jsonify(products), 200
            elif sorting == 'branddown':
                products = Product.query.filter(Product.ground.in_((groundFilter)), Product.price.between(pricefilterMin, pricefilterMax)).order_by(Product.brand.desc()).all()
                products = list(map(lambda product: product.serialize_w_categories(), products))
                return jsonify(products), 200  
        elif originFilter and groundFilter:
            if sorting == 'priceup':
                products = Product.query.filter(Product.origin.in_((originFilter)), Product.ground.in_((groundFilter)), Product.price.between(pricefilterMin, pricefilterMax)).order_by(Product.price.asc()).all()
                products = list(map(lambda product: product.serialize_w_categories(), products))
                return jsonify(products), 200
            elif sorting == 'pricedown':
                products = Product.query.filter(Product.origin.in_((originFilter)), Product.ground.in_((groundFilter)), Product.price.between(pricefilterMin, pricefilterMax)).order_by(Product.price.desc()).all()
                products = list(map(lambda product: product.serialize_w_categories(), products))
                return jsonify(products), 200
            elif sorting == 'brandup':
                products = Product.query.filter(Product.origin.in_((originFilter)), Product.ground.in_((groundFilter)), Product.price.between(pricefilterMin, pricefilterMax)).order_by(Product.brand.asc()).all()
                products = list(map(lambda product: product.serialize_w_categories(), products))
                return jsonify(products), 200
            elif sorting == 'branddown':
                products = Product.query.filter(Product.origin.in_((originFilter)), Product.ground.in_((groundFilter)), Product.price.between(pricefilterMin, pricefilterMax)).order_by(Product.brand.desc()).all()
                products = list(map(lambda product: product.serialize_w_categories(), products))
                return jsonify(products), 200                
        else:
            if sorting == 'priceup':
                products = Product.query.filter(Product.price.between(pricefilterMin, pricefilterMax)).order_by(Product.price.asc()).all()
                products = list(map(lambda product: product.serialize_w_categories(), products))
                return jsonify(products), 200
            elif sorting == 'pricedown':
                products = Product.query.filter(Product.price.between(pricefilterMin, pricefilterMax)).order_by(Product.price.desc()).all()
                products = list(map(lambda product: product.serialize_w_categories(), products))
                return jsonify(products), 200
            elif sorting == 'brandup':
                products = Product.query.filter(Product.price.between(pricefilterMin, pricefilterMax)).order_by(Product.brand.asc()).all()
                products = list(map(lambda product: product.serialize_w_categories(), products))
                return jsonify(products), 200
            elif sorting == 'branddown':
                products = Product.query.filter(Product.price.between(pricefilterMin, pricefilterMax)).order_by(Product.brand.desc()).all()
                products = list(map(lambda product: product.serialize_w_categories(), products))
                return jsonify(products), 200
        # here on is all to validate data on new products          
        if not sku and not price and not brand and not name and not presentation and not price and notstock and not origin and not species and not ground and not acidity and not roasting and not description:
            return jsonify({"msg": "some fields are missing"}), 400
        else:
            product= Product()
            product.sku= sku
            product.brand= brand
            product.name= name
            product.price= price
            product.stock= stock
            product.origin= origin
            product.species= species
            product.ground= ground
            product.acidity= acidity
            product.roasting= roasting
            product.presentation= presentation
            product.description= description
            product.image= image
            # this one make the realtionship between Product and Category models based on given category id, you MUST create a category before creating a product
            for category in categories:
                p_cat= Category.query.get(category)
                p_cat.category_id= category
                product.categories.append(p_cat)
            product.save()
            return jsonify(product.serialize_w_categories()), 201 
    if request.method == 'PUT':
        if not id:
            return jsonify({"msg": "product not found"}), 404
        else:
            sku= request.json.get("sku", None)
            brand= request.json.get("brand", None)
            name= request.json.get("name", None)
            presentation= request.json.get("presentation", None)
            price= request.json.get("price", None)
            stock= request.json.get("stock", None)
            origin= request.json.get("origin", None)
            species= request.json.get("species", None)
            ground= request.json.get("ground", None)
            acidity= request.json.get("acidity", None)
            roasting= request.json.get("roasting", None)
            description= request.json.get("description", None)
            image= request.json.get("image", None)
            # if not sku or price or brand or name or presentation or attributes or description or stock:
            if not sku:
                return jsonify({"msg": "some fields are missing"}), 400
            else:
                product= Product.query.get(id)
                product.sku= sku
                product.brand= brand
                product.name= name
                product.price= price
                product.stock= stock
                product.origin= origin
                product.species= species
                product.ground= ground
                product.acidity= acidity
                product.roasting= roasting
                product.presentation= presentation
                product.description= description
                product.image= image
                product.update()
                return jsonify(product.serialize()), 200
    if request.method == 'DELETE':
        product= Product.query.get(id)
        if not product:
            return jsonify({"msg": "Product not found"}), 404
        product.delete()
        return jsonify({"msg": "Product succesfully deleted"}), 200


# @app.route("/api/content", methods=['GET', 'POST', 'PUT', 'DELETE'])
@ app.route("/api/content/", methods=['GET', 'POST'])
@ app.route("/api/content/<id>", methods=['GET', 'PUT', 'DELETE'])
def content(id=None):
    if request.method == 'GET':
        if id is not None:
            content= Content.query.get(id)
            if content:
                return jsonify(content.serialize()), 200
            else:
                return jsonify({"msg": "content not found"}), 404
        else:
            content= Content.query.all()
            content= list(map(lambda content: content.serialize(), content))
            return jsonify(products), 200
    if request.method == 'POST':
        name=request.json.get("name", None)
        cover=request.json.get("cover", None)
        images=request.json.get("images", None)
        resume=request.json.get("resume", None)
        body=request.json.get("body", None)
        if not name and cover and images and resume and body:
            return jsonify({"msg": "some contents are missing"}), 400
        else:
            content=Content()
            content.name=name
            content.cover=cover
            content.images=images
            content.resume=resume
            content.body=body
            content.save()
            return jsonify(content.serialize()), 201
    if request.method == 'PUT':
        content=Content.query.get(id)
        if not content:
            return jsonify({"msg": "content not found"}), 404
        else:
            name=request.json.get("name", None)
            cover=request.json.get("cover", None)
            images=request.json.get("images", None)
            resume=request.json.get("resume", None)
            body=request.json.get("body", None)
        if not name and cover and images and resume and body:
            return jsonify({"msg": "some contents are missing"}), 400
        else:
            content=Content()
            content.name=name
            content.cover=cover
            content.images=images
            content.resume=resume
            content.body=body
            content.update()
            return jsonify(content.serialize()), 200
    if request.method == 'DELETE':
        content=Content.query.get(id)
        if not content:
            return jsonify({"msg": "Content not found"}), 404
        product.delete()
        return jsonify({"msg": "Content succesfully deleted"}), 200

# @app.route("/api/events", methods=['GET', 'POST', 'PUT', 'DELETE'])
if __name__ == "__main__":
    manager.run()
