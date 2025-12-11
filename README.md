# ms-auth-service

Microservicio dedicado a la autenticación (login) de usuarios.  
Expone un único endpoint para validar credenciales y emitir tokens JWT, reutilizando la misma base de datos de usuarios.

## Variables de entorno

- `DATABASE_URL`: cadena de conexión a la base de datos MySQL que contiene la tabla `users`.
- `SECRET_KEY`: clave usada para firmar los tokens JWT.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: duración de los tokens.
- `USER_SERVICE_URL`: URL base del microservicio de usuarios (por defecto `http://localhost:8000`). Si `ms-auth-service` se ejecuta dentro de Docker y `ms-user-service` corre en tu máquina local, usa `http://host.docker.internal:8000`; si ambos están dentro del mismo `docker compose`, usa el nombre del servicio (por ejemplo `http://ms-user-service:8000`).
- `INTERNAL_API_KEY`: clave compartida con `ms-user-service` para consumir su endpoint interno de validación de credenciales (`X-Internal-Secret`).

El `Docker-compose.yml` ya exporta estas variables con valores por defecto. Puedes sobrescribirlas creando un archivo `.env` junto al `docker compose` con los valores deseados.

## Ejecución local

```bash
cd ms-auth-service
uvicorn app.main:app --reload --port 8001
