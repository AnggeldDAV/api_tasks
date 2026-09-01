# API de gestión de usuarios y tareas

API REST desarrollada con FastAPI para la gestión de usuarios y tareas, con autenticación JWT, autorización por propietario de recursos, persistencia en PostgreSQL, tests automatizados y pipeline CI/CD.

El proyecto fue desarrollado como práctica personal para reforzar conocimientos de backend con Python y trabajar con herramientas y prácticas habituales en entornos profesionales.

## Demo

- API desplegada: https://api-tasks-xqul.onrender.com
- Documentación Swagger: https://api-tasks-xqul.onrender.com/docs

> La ruta raíz `/` no expone funcionalidad. La API se encuentra bajo el prefijo `/api/v1` y la documentación interactiva está disponible en `/docs`.

## Características principales

- API REST con FastAPI.
- CRUD de usuarios y tareas.
- Registro y login de usuarios.
- Autenticación mediante JWT.
- Contraseñas almacenadas mediante hash.
- Autorización basada en el propietario del recurso.
- Validación de datos mediante Pydantic.
- Persistencia con SQLAlchemy.
- PostgreSQL en producción.
- SQLite para tests.
- Tests automatizados con pytest.
- Documentación OpenAPI/Swagger.
- Health check.
- Integración continua con GitHub Actions.
- Despliegue automático en Render cuando los tests finalizan correctamente.

## Tecnologías

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- SQLite
- Pydantic / Pydantic Settings
- PyJWT
- bcrypt
- pytest
- HTTPX
- GitHub Actions
- Render

## Estructura del proyecto

La aplicación está organizada por responsabilidades:

```text
app/
├── api/
│   └── v1/
│       ├── api.py
│       ├── auth.py
│       ├── health.py
│       ├── task.py
│       └── user.py
├── core/
│   ├── security.py
│   └── settings.py
├── crud/
│   ├── task.py
│   └── user.py
├── db/
│   ├── database.py
│   └── init_db.py
├── deps/
│   └── deps.py
├── models/
│   ├── task.py
│   └── user.py
├── schemas/
│   ├── auth.py
│   ├── task.py
│   ├── token.py
│   └── user.py
└── main.py

tests/
├── conftest.py
├── test_auth.py
├── test_task.py
└── test_user.py

.github/
└── workflows/
    └── ci-cd.yml

.env.test
.gitignore
pytest.ini
requirements.txt
README.md
```

## Autenticación y autorización

La API utiliza JWT para autenticar las peticiones a endpoints protegidos.

Flujo general:

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
Verificación de credenciales
   ↓
JWT
   ↓
Authorization: Bearer <token>
   ↓
Endpoint protegido
```

El token permite identificar al usuario autenticado. A partir de ese usuario, la API aplica reglas de autorización para impedir el acceso, modificación o eliminación de recursos pertenecientes a otros usuarios.

Principales reglas:

- `POST /api/v1/users/` es público.
- Los endpoints protegidos requieren autenticación.
- Un usuario solo puede consultar, modificar o eliminar su propio usuario.
- Una tarea se asocia automáticamente al usuario autenticado.
- Un usuario solo puede consultar, modificar o eliminar sus propias tareas.
- Una petición sin autenticación devuelve `401`.
- Un usuario autenticado sin permisos devuelve `403`.
- Un recurso inexistente devuelve `404`.

## Endpoints principales

### Usuarios

```text
POST   /api/v1/users/
GET    /api/v1/users/
GET    /api/v1/users/{id}
PUT    /api/v1/users/{id}
DELETE /api/v1/users/{id}
```

### Tareas

```text
POST   /api/v1/tasks/
GET    /api/v1/tasks/
GET    /api/v1/tasks/{id}
PUT    /api/v1/tasks/{id}
DELETE /api/v1/tasks/{id}
```

### Autenticación

```text
POST /api/v1/auth/login
```

El login utiliza OAuth2 Password Flow y devuelve un token JWT:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

### Health check

```text
GET /api/v1/health
```

Respuesta:

```json
{
  "status": "ok"
}
```

La documentación completa y los esquemas de entrada/salida pueden consultarse directamente en Swagger.

## Tests

El proyecto utiliza pytest para realizar tests de API e integración.

Se comprueban, entre otros casos:

- creación, consulta, actualización y eliminación de usuarios;
- validación de datos;
- usuarios duplicados;
- login correcto e incorrecto;
- tokens JWT válidos e inválidos;
- acceso a endpoints protegidos;
- creación y gestión de tareas;
- aislamiento de tareas entre usuarios;
- acceso a recursos pertenecientes a otros usuarios;
- respuestas `403`, `404`, `409` y `422`.

Ejecutar los tests:

```bash
pytest
```

Los tests utilizan una base de datos SQLite independiente para no modificar los datos de desarrollo o producción.

## CI/CD

GitHub Actions ejecuta automáticamente los tests ante cambios en el repositorio.

```text
Push / Pull Request
        ↓
GitHub Actions
        ↓
Instalar dependencias
        ↓
pytest
     /      \
  FAIL      PASS
   ↓          ↓
 Stop       Deploy
              ↓
            Render
```

El despliegue a producción se ejecuta únicamente cuando:

- los tests han finalizado correctamente;
- el cambio corresponde a la rama `main`.

## Configuración

La aplicación utiliza variables de entorno para separar la configuración del código.

Ejemplo:

```text
DATABASE_URL=...
JWT_SECRET=...
ALGORITHM=HS256
```

Las variables sensibles de producción no se almacenan en el repositorio.

El archivo `.env.test` sí se mantiene versionado de forma intencionada porque contiene únicamente configuración no sensible utilizada por pytest y por el pipeline de CI. No debe contener credenciales reales ni secretos reutilizables fuera del entorno de testing.

## Instalación local

Clonar el repositorio:

```bash
git clone https://github.com/AnggeldDAV/api_tasks.git
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

Linux/macOS:

```bash
source venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Configurar las variables de entorno necesarias y ejecutar la aplicación:

```bash
uvicorn main:app --app-dir app --reload
```

Swagger estará disponible en:

```text
http://127.0.0.1:8000/docs
```

## Decisiones técnicas

### PostgreSQL en producción y SQLite en tests

La aplicación utiliza PostgreSQL como base de datos de producción y una base de datos SQLite independiente durante los tests. Esto permite ejecutar la suite de pruebas sin modificar datos reales ni depender de la base de datos desplegada.

### Autorización basada en el usuario autenticado

El `user_id` de una tarea no se recibe desde el cliente al crearla. La API obtiene el usuario a partir del JWT y asigna automáticamente la tarea a ese usuario. Las consultas a tareas se filtran en la base de datos para devolver únicamente los recursos permitidos.

### Separación por responsabilidades

El proyecto separa routers, modelos, schemas, acceso a datos, dependencias, configuración y seguridad para evitar concentrar toda la lógica en los endpoints y facilitar el mantenimiento del código.

### CI antes del despliegue

El pipeline obliga a que los tests finalicen correctamente antes de ejecutar el despliegue a Render, evitando desplegar automáticamente cambios que rompan la suite de pruebas.

## Próximas mejoras

- Migraciones de base de datos mediante Alembic.
- Paginación de resultados.
- Filtros y ordenación de tareas.
- Tests unitarios adicionales.
- Mejoras de logging y observabilidad.
- Integración del health check directamente en el proceso de despliegue.
- Dockerización completa del entorno de desarrollo.

## Objetivo del proyecto

El objetivo principal ha sido pasar de seguir ejemplos completos a desarrollar una aplicación backend tomando decisiones propias, consultando documentación y resolviendo problemas de implementación de forma progresivamente más autónoma.
