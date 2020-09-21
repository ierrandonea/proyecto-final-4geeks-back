import json, datetime
from flask import Flask, request, jsonify, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from models import db, Users
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

    user = Users.query.filter_by(email = email).first()

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
    
    user = Users.query.filter_by(email = email).first()
    print(user)

    if user:
        return jsonify({"msg": "User already exists"}), 400

    user = Users()
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
    user = Users.query.get(id)
    return jsonify(user.serialize()), 200 

# @app.route("/api/users", methods=['GET', 'POST', 'PUT', 'DELETE'])

# @app.route("/api/products", methods=['GET', 'POST', 'PUT', 'DELETE'])
# @app.route("/api/content", methods=['GET', 'POST', 'PUT', 'DELETE'])
# @app.route("/api/events", methods=['GET', 'POST', 'PUT', 'DELETE'])

if __name__ == "__main__":
    manager.run()
 