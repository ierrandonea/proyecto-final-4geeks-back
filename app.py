import json
from flask import Flask, request, jsonify, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, User
from config import Development

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(Development)

db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
CORS(app)

@app.route("/api/users", methods=['GET', 'POST', 'PUT', 'DELETE'])

@app.route("/api/products", methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route("/api/content", methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route("/api/events", methods=['GET', 'POST', 'PUT', 'DELETE'])

if __name__ == "__main__":
    manager.run()
 