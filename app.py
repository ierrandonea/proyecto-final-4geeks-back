import json, os, datetime
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
        
@app.route("/api/products/", methods=['GET', 'POST'])
@app.route("/api/products/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def products(id = None):
    if request.method == 'GET':
        if id is not None:
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
        attributes = request.json.get("attributes", None)
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
            product.presentation = json.dumps(presentation)
            product.attributes = json.dumps(attributes)
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
            attributes = request.json.get("attributes", None)
            description = request.json.get("description", None)
            image = request.json.get("image", None)
            stock = request.json.get("stock", None)  
            # if not sku or price or brand or name or presentation or attributes or description or stock:
            if not sku:
                return jsonify({"msg": "some fields are missing"}), 400
            else:                                
                product = Product.query.get(id)
                product.sku = sku
                product.brand = brand
                product.name = name
                product.presentation = json.dumps(presentation)
                product.attributes = json.dumps(attributes)
                product.description = description
                product.image = image
                product.stock = stock
                product.update()
                return jsonify(product.serialize()), 200
    if request.method == 'DELETE':
        product = Product.query.get(id)
        if not product:
            return jsonify({"msg": "Product not found"}), 404
        product.delete()
        return jsonify({"msg": "Product succesfully deleted"}), 200
# @app.route("/api/content", methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route("/api/content/", methods=['GET', 'POST'])
@app.route("/api/content/<id>", methods=['GET', 'PUT', 'DELETE'])
def content (id=None):
    if request.method == 'GET':
        if id is not None:
            content = Content.query.get(id)
            if content: 
                return jsonify(content.serialize()), 200
            else:
                return jsonify({"msg": "content not found"}), 404
        else:
            content = Content.query.all()
            content = list(map(lambda content: content.serialize(), content))
            return jsonify(products), 200
    if request.method == 'POST':
        name = request.json.get("name", None)
        cover = request.json.get("cover", None)
        images = request.json.get("images", None)
        resume = request.json.get("resume", None)
        body = request.json.get("body", None)
        if not name and cover and images and resume and body:
            return jsonify({"msg":"some contents are missing"}), 400
        else:
            content = Content()
            content.name = name
            content.cover = cover
            content.images = images
            content.resume = resume
            content.body = body
            content.save()
            return jsonify(content.serialize()), 201
    if request.method == 'PUT':
        content = Content.query.get(id)
        if not content:
            return jsonify({"msg":"content not found"}), 404
        else:
            name = request.json.get("name", None)
            cover = request.json.get("cover", None)
            images = request.json.get("images", None)
            resume = request.json.get("resume", None)
            body = request.json.get("body", None)
        if not name and cover and images and resume and body:
            return jsonify({"msg":"some contents are missing"}), 400
        else:
            content = Content()
            content.name = name
            content.cover = cover
            content.images = images
            content.resume = resume
            content.body = body
            content.update()
            return jsonify(content.serialize()), 200 
    if request.method == 'DELETE':
        content = Content.query.get(id)
        if not content:
            return jsonify({"msg": "Content not found"}), 404
        product.delete()
        return jsonify({"msg": "Content succesfully deleted"}), 200

# @app.route("/api/events", methods=['GET', 'POST', 'PUT', 'DELETE'])
if __name__ == "__main__":

    manager.run()


# {
# 	"attributes": {
# 		"acidity": "7",
# 		"origin": "Colombia",
# 		"roasting": "65 AGS",
# 		"species": "Robusta",
# 		"type": "Molido"
# 	},
# 	"brand": "Finca Test",
# 	"description": "Lorem ipsum dolor sit amen.",
# 	"image": "base_placeholder-Cecilia-Lorenzo-Inaki.jpg",
# 	"name": "Debugging coffee",
# 	"presentation": [
# 		{
# 			"format1": "150gr",
# 			"stock": 16,
# 			"price": "5600"
# 		},
# 		{
# 			"format2": "260gr",
# 			"stock": 14,
# 			"price": "9600"
# 		},
# 		{
# 			"format3": "1kg",
# 			"stock": 9,
# 			"price": "15000"
# 		}
# 	],
# 	"sku": "4gB-FP-4Geeks-a11",
# 	"categories": [1,2]
# }

# [
#   {
#     "attributes": {
#       "acidity": "6",
#       "origin": "Colombia",
#       "roasting": "95 AGS",
#       "species": "Arabica",
#       "type": "Molido"
#     },
#     "brand": "4Geeks Coffee",
#     "description": "Lorem ipsum dolor sit amen.",
#     "id": 1,
#     "image": "base_placeholder-Cecilia-Lorenzo-Inaki.jpg",
#     "name": "Console.log(Coffee)",
#     "presentation": [
#       {
#         "format": "100gr",
#         "stock": 22
#       },
#       {
#         "format": "210gr",
#         "stock": 10
#       },
#       {
#         "format": "370gr",
#         "stock": 19
#       }
#     ],
#     "sku": "4gB-FP-4Geeks-ftVII"
#   },
#   {
#     "attributes": {
#       "acidity": "6",
#       "origin": "Perú",
#       "roasting": "75 AGS",
#       "species": "Arabica",
#       "type": "Grano"
#     },
#     "brand": "Los Cafetales de Satán",
#     "description": "Lorem ipsum dolor sit amen.",
#     "id": 2,
#     "image": "base_placeholder-Cecilia-Lorenzo-Inaki.jpg",
#     "name": "Café Cecilia",
#     "presentation": [
#       {
#         "format": "120gr",
#         "stock": 14
#       },
#       {
#         "format": "250gr",
#         "stock": 11
#       },
#       {
#         "format": "480gr",
#         "stock": 12
#       }
#     ],
#     "sku": "4gB-FP-Ca2Lo3Ii4-ftVII"
#   },
#   {
#     "attributes": {
#       "acidity": "9",
#       "origin": "Venelueza",
#       "roasting": "75 AGS",
#       "species": "Arabica",
#       "type": "Grano"
#     },
#     "brand": "Los Cafetales de Satán",
#     "description": "Lorem ipsum dolor sit amen.",
#     "id": 3,
#     "image": "base_placeholder-Cecilia-Lorenzo-Inaki.jpg",
#     "name": "Café de Lorenzo",
#     "presentation": [
#       {
#         "format": "150gr",
#         "stock": 34
#       },
#       {
#         "format": "250gr",
#         "stock": 18
#       },
#       {
#         "format": "500gr",
#         "stock": 7
#       }
#     ],
#     "sku": "4gB-FP-Ca1Lo2Ii3-ft7"
#   },
#   {
#     "attributes": {
#       "acidity": "6",
#       "origin": "Chile",
#       "roasting": "55 AGS",
#       "species": "Arabica",
#       "type": "Cápsulas"
#     },
#     "brand": "Los Cafetales de Satán",
#     "description": "Lorem ipsum dolor sit amen.",
#     "id": 4,
#     "image": "base_placeholder-Cecilia-Lorenzo-Inaki.jpg",
#     "name": "Iñaki Café",
#     "presentation": [
#       {
#         "format": "12u",
#         "stock": 12
#       },
#       {
#         "format": "21u",
#         "stock": 8
#       },
#       {
#         "format": "30u",
#         "stock": 21
#       }
#     ],
#     "sku": "4gB-FP-Ca7Lo8Ii9-ft14"
#   },
#   {
#     "attributes": {
#       "acidity": "5",
#       "origin": "Chile-Venezuela",
#       "roasting": "65 AGS",
#       "species": "Arabica",
#       "type": "Cápsulas"
#     },
#     "brand": "4Geeks Coffee",
#     "description": "Lorem ipsum dolor sit amen.",
#     "id": 5,
#     "image": "base_placeholder-Cecilia-Lorenzo-Inaki.jpg",
#     "name": "Monroy Café",
#     "presentation": [
#       {
#         "format": "12u",
#         "stock": 10
#       },
#       {
#         "format": "25u",
#         "stock": 18
#       },
#       {
#         "format": "35u",
#         "stock": 12
#       }
#     ],
#     "sku": "4gB-FP-4Geeks-ft21"
#   },
#   {
#     "attributes": {
#       "acidity": "7",
#       "origin": "Chile-Venezuela",
#       "roasting": "85 AGS",
#       "species": "Arabica",
#       "type": "Grano"
#     },
#     "brand": "4Geeks Coffee",
#     "description": "Lorem ipsum dolor sit amen.",
#     "id": 6,
#     "image": "base_placeholder-Cecilia-Lorenzo-Inaki.jpg",
#     "name": "Café LJGoku",
#     "presentation": [
#       {
#         "format1": "120gr",
#         "stock": 15
#       },
#       {
#         "format2": "240gr",
#         "stock": 18
#       },
#       {
#         "format3": "480gr",
#         "stock": 7
#       }
#     ],
#     "sku": "4gB-FP-4Geeks-a11"
#   }
# ]