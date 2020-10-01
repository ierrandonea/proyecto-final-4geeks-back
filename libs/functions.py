from flask_jwt_extended import get_jwt_identity
from models import User

def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def isAdmin():
    id = get_jwt_identity()
    user = User.query.get(id)    
    return True if user.role == "isAdmin" else False 