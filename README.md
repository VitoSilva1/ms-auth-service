# ms-auth-service

Microservicio dedicado a la autenticación (login) de usuarios. Expone un único endpoint para validar credenciales y emitir tokens JWT, reutilizando la misma base de datos de usuarios.

## Variables de entorno

- `DATABASE_URL`: cadena de conexión a la base de datos MySQL que contiene la tabla `users`.
- `SECRET_KEY`: clave usada para firmar los tokens JWT.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: duración de los tokens.

## Ejecución local

```bash
cd ms-auth-service
uvicorn app.main:app --reload --port 8001
```

Alternativamente puedes usar Docker Compose:

```bash
cd ms-auth-service
docker compose up --build
```

Esto expone el servicio en `http://localhost:8001` y levanta un contenedor de MySQL aislado.

## Endpoint principal

- `POST /auth/login`: recibe `email` y `password`, y devuelve un token JWT (`access_token`, `token_type`).

El microservicio consulta directamente la tabla `users`, por lo que depende de que el `ms-user-service` se encargue de crear y administrar los registros.
