# API de gestion de usuarios y tareas

API REST desarrollada con FastAPI para la gestion de usuarios y tareas, incluyendo autenticacion mediante JWT, autorizacion basada en el usuario propietario de los recursos, persistencia en PostgreSQL, tests automatizados y pipeline CI/CD.

El proyecto ha sido desarrollado como proyecto practico para mejorar conocimientos de desarrollo backend con Python y adquirir experiencia con herramientas y practicas utilizadas en entornos profesionales.

## Caracteristicas

- API REST desarrollada con FastAPI.
- Gestion de usuarios.
- Gestion de tareas asociadas a usuarios.
- Registro y autenticacion de usuarios.
- Autenticacion mediante JWT.
- Contraseñas almacenadas mediante hash.
- Autorizacion para impedir el acceso a recursos de otros usuarios.
- Validacion de datos mediante Pydantic.
- Persistencia mediante SQLAlchemy.
- PostgreSQL como base de datos de produccion.
- SQLite utilizada para los tests.
- Tests automatizados con pytest.
- Tests de endpoints, validaciones, autenticacion y autorizacion.
- Documentacion interactiva mediante Swagger/OpenAPI.
- Endpoint de health check.
- Integracion continua mediante GitHub Actions.
- Despliegue automatico en Render despues de superar los tests.

## Tecnologias

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic / Pydantic Settings
- JWT
- bcrypt
- pytest
- HTTPX
- GitHub Actions
- Render

## Estructura del proyecto

La estructura principal del proyecto sigue una separacion por responsabilidades:
```text
app/
├── api/
│   └── v1/
│       ├── api.py
│       ├── auth.py
│       ├── health.py
│       ├── task.py
│       └── user.py
│
├── core/
│   ├── security.py
│   └── settings.py
│
├── crud/
│   ├── task.py
│   └── user.py
│
├── db/
│   ├── database.py
│   └── init_db.py
│
├── deps/
│   └── deps.py
│
├── models/
│   ├── task.py
│   └── user.py
│
├── schemas/
│   ├── auth.py
│   ├── task.py
│   ├── token.py
│   └── user.py
│
└── main.py

tests/
├── conftest.py
├── test_auth.py
├── test_task.py
└── test_user.py

.github/
└── workflows/
    └── ci-cd.yml

.env
.env.test
.gitignore
pytest.ini
requirements.txt
README.md
```
## Enrutador principal de la API

El archivo `app/api/v1/api.py` contiene el enrutador principal que agrega todos los enrutadores de los distintos recursos de la API. Cada enrutador se incluye con un prefijo y etiquetas para la documentacion automatica.

```python
from fastapi import APIRouter
from api.v1 import task, user, auth, health

api_router = APIRouter()

api_router.include_router(user.api_router, prefix="/users", tags=["users"])
api_router.include_router(task.api_router, prefix="/tasks", tags=["tasks"])
api_router.include_router(auth.api_router, prefix="/auth", tags=["auth"])
api_router.include_router(health.api_router, prefix="/health", tags=["health"])
```
Este enrutador principal se monta en la aplicacion FastAPI dentro de app/main.py bajo el prefijo /api/v1, de modo que todas las rutas definidas en los enrutadores quedan disponibles bajo esa base.
## Autenticacion

La API utiliza JWT (JSON Web Tokens) para autenticar las peticiones a endpoints protegidos.

El flujo es:
```text
Registro
   ↓
Usuario + contraseña
   ↓
Hash de contraseña
   ↓
Base de datos

Login
   ↓
Usuario + contraseña
   ↓
Verificacion
   ↓
JWT
   ↓
Authorization: Bearer <token>
   ↓
Endpoint protegido
```

Las contraseñas no se almacenan directamente, sino mediante un hash.

Los endpoints protegidos obtienen el usuario actual a partir del JWT y utilizan su identificador para comprobar que puede acceder al recurso solicitado.

## Usuarios

### Crear usuario

`POST /api/v1/users/`

Endpoint publico.

Ejemplo:
```json
{
  "name": "usuario",
  "password": "password123"
}
```
Respuesta:
```json
{
  "id": 1,
  "name": "usuario"
}
```

### Obtener usuarios

`GET /api/v1/users/`

Requiere autenticacion.

### Obtener usuario

`GET /api/v1/users/{id}`

El usuario autenticado solamente puede consultar su propio usuario.

### Actualizar usuario

`PUT /api/v1/users/{id}`

El usuario solamente puede modificar su propia informacion.

### Eliminar usuario

`DELETE /api/v1/users/{id}`

El usuario solamente puede eliminar su propia cuenta.

## Tareas

Las tareas pertenecen a un usuario.

### Crear tarea

`POST /api/v1/tasks/`

Requiere autenticacion.

La tarea se asocia automaticamente al usuario obtenido del JWT.

Ejemplo:
```json
{
  "title": "Implementar tests",
  "description": "Crear tests para la API",
  "state": "in_progress",
  "priority": true,
  "date": "2026-01-01T00:00:00"
}
```

### Obtener tareas

`GET /api/v1/tasks/`

Devuelve unicamente las tareas pertenecientes al usuario autenticado.

### Obtener una tarea

`GET /api/v1/tasks/{id}`

El usuario solamente puede acceder a sus propias tareas.

### Actualizar tarea

`PUT /api/v1/tasks/{id}`

El usuario solamente puede modificar sus propias tareas.

### Eliminar tarea

`DELETE /api/v1/tasks/{id}`

El usuario solamente puede eliminar sus propias tareas.

## Login

`POST /api/v1/auth/login`

Utiliza el flujo OAuth2 Password y recibe las credenciales mediante formulario.

Una autenticacion correcta devuelve un token JWT:
```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

Este token debe enviarse posteriormente mediante:

Authorization: Bearer <token>

## Health Check

La API dispone de un endpoint para comprobar que el servicio esta funcionando:

`GET /api/v1/health`

Respuesta:
```json
{
  "status": "ok"
}
```

## Tests

El proyecto utiliza pytest para realizar tests automatizados.

Los tests cubren principalmente:

- Creacion de usuarios.

- Validacion de datos.

- Usuarios duplicados.

- Consulta de usuarios.

- Actualizacion y eliminacion.

- Control de permisos.

- Creacion de tareas.

- Filtrado de tareas por usuario.

- Validacion de tareas.

- Autenticacion.

- Login correcto e incorrecto.

- Tokens JWT validos e invalidos.

- Acceso a endpoints protegidos.

- Usuarios inexistentes.

- Recursos pertenecientes a otros usuarios.

Para ejecutar los tests:

```bash
pytest
```

Los tests utilizan una base de datos independiente para evitar modificar los datos de desarrollo o produccion.

## CI/CD

El proyecto utiliza GitHub Actions para automatizar la ejecucion de tests y el despliegue.

El flujo implementado es:
```text
             Push / Pull Request
                      │
                      ▼
               GitHub Actions
                      │
                      ▼
             Instalar dependencias
                      │
                      ▼
                   pytest
                  /     \
               FAIL     PASS
                │         │
                ▼         ▼
             Stop      Deploy
                           │
                           ▼
                         Render
```

Los tests se ejecutan automaticamente ante cambios en el repositorio.

El despliegue a produccion solamente se realiza cuando:

- Los tests han terminado correctamente.

- El cambio corresponde a la rama main.

## Configuracion

La aplicacion utiliza variables de entorno para la configuracion sensible.

Ejemplo:
```text
DATABASE_URL=...
JWT_SECRET=...
ALGORITHM=HS256
```

Las variables de entorno no se almacenan en el repositorio.

Para ejecutar los tests se utiliza una configuracion independiente mediante `.env.test.`

## Instalacion local

Clonar el repositorio:
```bash
git clone <repository-url>
cd api_tasks
```

Crear y activar un entorno virtual:
```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Instalar las dependencias:
```bash
pip install -r requirements.txt
```

Configurar las variables de entorno y ejecutar la aplicacion:
```bash
uvicorn main:app --app-dir app --reload
```

La documentacion interactiva estara disponible en:
```text
http://127.0.0.1:8000/docs
```

## Documentacion de la API
FastAPI genera automaticamente documentacion OpenAPI.

Durante el desarrollo puede utilizarse Swagger UI:
```text
/docs
```

Desde Swagger es posible consultar los endpoints y probar el sistema de autenticacion.

## Despliegue

La aplicacion esta preparada para ejecutarse en Render utilizando PostgreSQL como base de datos.

El despliegue se integra con GitHub Actions:
```text
GitHub
   ↓
GitHub Actions
   ↓
pytest
   ↓
Render Deploy Hook
   ↓
Produccion
```
Las credenciales y variables sensibles se gestionan mediante variables de entorno del entorno de produccion.

## Objetivos del proyecto

Este proyecto se ha desarrollado con los siguientes objetivos:

- Mejorar conocimientos de Python y FastAPI.

- Comprender el desarrollo de APIs REST.

- Trabajar con bases de datos relacionales mediante SQLAlchemy.

- Implementar autenticacion y autorizacion.

- Aprender testing automatizado.

- Familiarizarse con CI/CD.

- Realizar un despliegue real de una aplicacion backend.

- Aplicar una estructura de proyecto mantenible y separada por responsabilidades.

## Proximas mejoras
Algunas mejoras que podrian incorporarse en futuras versiones:

- Migraciones de base de datos mediante Alembic.

- Paginacion de resultados.

- Filtros y ordenacion de tareas.

- Tests adicionales a nivel unitario.

- Mejoras en logging y observabilidad.

- Endpoint de health check utilizado directamente dentro del pipeline de despliegue.

## Proyecto personal
Proyecto desarrollado como parte de mi aprendizaje y preparacion al desarrollo backend con Python.