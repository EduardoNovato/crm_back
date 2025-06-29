# CRM Backend

Este proyecto es el backend de un CRM sencillo desarrollado en Python utilizando Flask. Su objetivo es servir como base para la gestión de usuarios y autenticación en un sistema CRM.

## Características principales

- API RESTful construida con Flask y Flask-RESTX
- Autenticación y autorización mediante JWT (Flask-JWT-Extended)
- Gestión de usuarios: registro y login
- ORM con SQLAlchemy

## Estructura del proyecto

```
crm_back/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── jwt_callbacks.py
│   ├── models/
│   │   └── user.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   └── user_routes.py
│   └── utils/
│       ├── decorators.py
│       └── validators.py
├── run.py
├── requirements.txt
├── readme.md
└── run.sh
```

## Instalación y Uso

1. Clona el repositorio y entra en la carpeta del proyecto.
2. Ejecuta el script de instalación y arranque:
   ```bash
   ./run.sh
   ```

## Endpoints principales

Aqui encontraras todas las rutas disponibles
- http://127.0.0.1:5000/docs

## Dependencias principales

- Flask
- Flask-RESTX
- Flask-JWT-Extended
- Flask-SQLAlchemy

## Notas

Por ahora, el backend solo implementa la autenticación y la creación de usuarios. Próximamente se agregarán más funcionalidades para la gestión de clientes, oportunidades y otras entidades del CRM.

---

Desarrollado por [EduardoNovato]
