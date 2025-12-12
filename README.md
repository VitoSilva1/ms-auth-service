# ms-auth-service

Microservicio FastAPI responsable del **login** y la emisión de tokens JWT para el ecosistema Fintruck. Su única responsabilidad es autenticar credenciales contra `ms-user-service` y devolver un `access_token` firmado para que el resto de servicios valide permisos.

## Características
- Endpoint único `POST /auth/login` con validaciones claras para credenciales inválidas (`401`) y fallos del servicio de usuarios (`503`).
- Firma de tokens con `python-jose` y expiración configurable.
- Creación de tablas en el arranque con reintentos (`app/main.py`) para tolerar retrasos del motor MySQL cuando se levanta con Docker.

## Variables de entorno

| Variable | Descripción |
| --- | --- |
| `DATABASE_URL` | Cadena de conexión MySQL usada solo para crear la tabla `users` requerida por SQLAlchemy. |
| `SECRET_KEY` | Clave privada para firmar los tokens JWT. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tiempo de expiración del token. |
| `USER_SERVICE_URL` | URL base del `ms-user-service`. Usa `http://host.docker.internal:8000` cuando auth corre en contenedor y user en la máquina host. |
| `INTERNAL_API_KEY` | Clave compartida para consumir `/users/internal/authenticate` mediante el header `X-Internal-Secret`. |

Todas las variables tienen valores por defecto en `.env` y `Docker-compose.yml`, pero puedes sobreescribirlas con tu propio archivo `.env`.

## Ejecución

### Local (sin Docker)
```bash
cd BackendFinTrack/ms-auth-service
python3 -m venv .venv && source .venv/bin/activate  # opcional
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

### Docker Compose
```bash
cd BackendFinTrack/ms-auth-service
docker compose up --build
```

## Pruebas unitarias
Se incluyen pruebas básicas para `app/services/auth_service.py` en `auth_test.py`. Ejecuta:
```bash
cd BackendFinTrack/ms-auth-service
python3 auth_test.py
```
Las pruebas utilizan `unittest` y mocks sobre `httpx.post` para cubrir los casos de éxito, credenciales inválidas, errores del servicio remoto y fallas de red.

## Endpoint principal

`POST /auth/login`

**Request**
```json
{
  "email": "admin@fintruck.com",
  "password": "secret"
}
```

**Response 200**
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

Utiliza el token en el header `Authorization: Bearer <jwt>` para consumir los demás microservicios. Ante un error del servicio de usuarios recibirás `503 Service Unavailable` con un mensaje descriptivo.
