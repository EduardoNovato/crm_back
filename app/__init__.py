from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restx import Api
from dotenv import load_dotenv
from .config import Config
from .jwt_callbacks import register_jwt_callbacks

# Extensiones globales
db = SQLAlchemy()
jwt = JWTManager()

authorizations = {
    'BearerAuth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'JWT Authorization header usando el esquema Bearer. Ejemplo: "Bearer {token}"'
    }
}

api = Api(
    version='1.0',
    title='CRM Backend API',
    description='API para autenticación y gestión de usuarios con JWT',
    doc='/docs',
    prefix='/api/v1',
    authorizations=authorizations,
    security='BearerAuth'  # ← Aplica por defecto a todos los endpoints
)

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    # Registrar callbacks JWT
    register_jwt_callbacks(jwt)

    with app.app_context():
        from .models.user import User
        db.create_all()

    from .routes.auth_routes import auth_ns
    from .routes.user_routes import user_ns
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(user_ns, path='/api/v1/users')

    return app
