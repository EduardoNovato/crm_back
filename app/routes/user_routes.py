from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import User
from ..utils.decorators import admin_required

user_ns = Namespace('users', description='Operaciones de usuarios')

user_model = user_ns.model('User', {
    'id': fields.Integer,
    'email': fields.String,
    'username': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'role': fields.String,
    'is_active': fields.Boolean,
    'created_at': fields.String,
    'last_login': fields.String
})

@user_ns.doc(security='BearerAuth')
@user_ns.route('/profile')
class UserProfile(Resource):
    @jwt_required()
    @user_ns.marshal_with(user_model)
    def get(self):
        user = User.query.get(get_jwt_identity())
        if not user:
            return {'message': 'Usuario no encontrado'}, 404
        return user.to_dict()

@user_ns.doc(security='BearerAuth')
@user_ns.route('/users')
class UserList(Resource):
    @admin_required
    def get(self):
        users = User.query.all()
        return {
            'users': [u.to_dict() for u in users],
            'total': len(users)
        }

@user_ns.doc(security='BearerAuth')
@user_ns.route('/users/<int:user_id>')
class UserDetail(Resource):
    @admin_required
    @user_ns.marshal_with(user_model)
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'Usuario no encontrado'}, 404
        return user.to_dict()

@user_ns.doc(security='BearerAuth')
@user_ns.route('/protected')
class ProtectedExample(Resource):
    @jwt_required()
    def get(self):
        user = User.query.get(get_jwt_identity())
        return {
            'message': f'Hola {user.first_name}, tienes acceso autorizado.',
            'user_id': user.id
        }
