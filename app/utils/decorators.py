from functools import wraps
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import jsonify
from ..models.user import User

def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user = User.query.get(get_jwt_identity())
        if not user or user.role != 'admin':
            return {'message': 'Se requieren permisos de administrador'}, 403
        return f(*args, **kwargs)
    return decorated_function