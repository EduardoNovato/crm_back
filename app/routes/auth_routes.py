from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from datetime import datetime
from .. import db
from ..models.user import User
from ..utils.validators import validate_email, validate_password
from ..jwt_callbacks import blacklisted_tokens
from flask import current_app

auth_ns = Namespace('auth', description='Operaciones de autenticación')

# Modelos Swagger
register_model = auth_ns.model('Register', {
    'email': fields.String(required=True),
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True)
})

login_model = auth_ns.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

token_response = auth_ns.model('TokenResponse', {
    'access_token': fields.String,
    'refresh_token': fields.String,
    'expires_in': fields.Integer,
    'user': fields.Raw
})

message_response = auth_ns.model('MessageResponse', {
    'message': fields.String,
    'status': fields.String
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model)
    @auth_ns.response(201, 'Registrado', message_response)
    @auth_ns.response(400, 'Datos inválidos')
    @auth_ns.response(409, 'Usuario ya existe')
    def post(self):
        data = request.get_json()

        for field in ['email', 'username', 'password', 'first_name', 'last_name']:
            if not data.get(field):
                return {'message': f'El campo {field} es requerido'}, 400

        if not validate_email(data['email']):
            return {'message': 'Email inválido'}, 400

        is_valid, msg = validate_password(data['password'])
        if not is_valid:
            return {'message': msg}, 400

        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Email ya registrado'}, 409

        if User.query.filter_by(username=data['username']).first():
            return {'message': 'Username ya en uso'}, 409

        user = User(
            email=data['email'].lower(),
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        return {'message': 'Usuario registrado exitosamente', 'status': 'success'}, 201

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'Login exitoso', token_response)
    @auth_ns.response(401, 'Credenciales inválidas')
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email'].lower()).first()

        if not user or not user.check_password(data['password']):
            return {'message': 'Credenciales inválidas'}, 401

        if not user.is_active:
            return {'message': 'Cuenta desactivada'}, 401

        user.last_login = datetime.utcnow()
        db.session.commit()

        access_token = create_access_token(identity=user.id, additional_claims={'role': user.role})
        refresh_token = create_access_token(identity=user.id, expires_delta=current_app.config['JWT_REFRESH_TOKEN_EXPIRES'])

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': int(current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()),
            'user': user.to_dict()
        }, 200

@auth_ns.route('/logout')
class Logout(Resource):
    @jwt_required()
    @auth_ns.response(200, 'Logout exitoso')
    def post(self):
        jti = get_jwt()['jti']
        blacklisted_tokens.add(jti)
        return {'message': 'Sesión cerrada exitosamente', 'status': 'success'}, 200

@auth_ns.route('/refresh')
class Refresh(Resource):
    @jwt_required()
    @auth_ns.response(200, 'Token renovado')
    def post(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user or not user.is_active:
            return {'message': 'Usuario no válido'}, 401

        new_token = create_access_token(identity=user.id, additional_claims={'role': user.role})
        return {
            'access_token': new_token,
            'expires_in': int(db.app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()),
            'user': user.to_dict()
        }, 200
