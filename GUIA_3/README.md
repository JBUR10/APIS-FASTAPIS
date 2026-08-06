# API CRUD con FastAPI y Seguridad JWT

Este proyecto consiste en una API REST desarrollada con **FastAPI** para gestionar productos, categorías, proveedores y empleados mediante operaciones CRUD (Crear, Leer, Actualizar y Eliminar).

Además, implementa mecanismos de seguridad utilizando:

- Autenticación mediante JWT (JSON Web Token).
- Autorización basada en roles.
- Hashing de contraseñas con bcrypt.
- Protección de endpoints mediante Depends de FastAPI.

---

# Requisitos

- Python 3.10 o superior
- FastAPI
- Uvicorn
- bcrypt
- PyJWT
- python-multipart

---

# Instalación

Instala las dependencias con el siguiente comando:

```bash
pip install fastapi uvicorn bcrypt pyjwt python-multipart
```

---

# Ejecución

Inicia el servidor con alguno de estos comandos:

```bash
uvicorn main:app --reload
```

o

```bash
python -m uvicorn main:app --reload
```

La aplicación estará disponible en:

- http://127.0.0.1:8000

---

# Documentación

FastAPI genera automáticamente la documentación interactiva de la API.

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

Desde Swagger UI es posible iniciar sesión utilizando el botón **Authorize**.

---

# Seguridad Implementada

## Autenticación

La autenticación permite verificar la identidad del usuario mediante nombre de usuario y contraseña.

Al iniciar sesión correctamente, el sistema genera un token JWT que debe enviarse en las peticiones protegidas.

## Autorización

La autorización determina qué acciones puede realizar cada usuario según su rol.

### Roles disponibles

- **admin**
  - Puede crear, editar y eliminar registros.
- **cliente**
  - Puede crear y editar registros.
  - No puede eliminar registros.

## Hashing de Contraseñas

Las contraseñas no se almacenan en texto plano.

Se utiliza **bcrypt** para generar hashes seguros y verificar credenciales durante el inicio de sesión.

---

# Usuarios de Prueba

## Administrador

```text
Usuario: admin
Contraseña: admin123
Rol: admin
```

## Cliente

```text
Usuario: joel
Contraseña: joel123
Rol: cliente
```

---

# Endpoints de Autenticación

## Login

```http
POST /auth/login
```

Permite iniciar sesión y obtener un token JWT.

## Registro

```http
POST /auth/registro
```

Permite registrar nuevos usuarios con rol cliente.

## Quién Soy

```http
GET /auth/yo
```

Endpoint protegido que devuelve la información del usuario autenticado.

---

# Endpoints de Productos

| Método | Endpoint | Acceso |
|---------|----------|---------|
| GET | /productos | Público |
| GET | /productos/{id} | Público |
| POST | /productos | Autenticado |
| PUT | /productos/{id} | Autenticado |
| DELETE | /productos/{id} | Solo Admin |

---

# Endpoints de Categorías

| Método | Endpoint | Acceso |
|---------|----------|---------|
| GET | /categorias | Público |
| GET | /categorias/{id} | Público |
| POST | /categorias | Autenticado |
| PUT | /categorias/{id} | Autenticado |
| DELETE | /categorias/{id} | Solo Admin |

---

# Endpoints de Proveedores

| Método | Endpoint | Acceso |
|---------|----------|---------|
| GET | /proveedores | Público |
| GET | /proveedores/{id} | Público |
| POST | /proveedores | Autenticado |
| PUT | /proveedores/{id} | Autenticado |
| DELETE | /proveedores/{id} | Solo Admin |

---

# Endpoints de Empleados

| Método | Endpoint | Acceso |
|---------|----------|---------|
| GET | /empleados | Público |
| GET | /empleados/{id} | Público |
| POST | /empleados | Autenticado |
| PUT | /empleados/{id} | Autenticado |
| DELETE | /empleados/{id} | Solo Admin |

---

# Códigos de Respuesta

| Código | Significado |
|---------|-------------|
| 200 | Operación exitosa |
| 201 | Recurso creado correctamente |
| 401 | No autenticado o token inválido |
| 403 | Usuario sin permisos suficientes |
| 404 | Recurso no encontrado |
| 422 | Datos inválidos enviados al endpoint |

---

# Tecnologías Utilizadas

- FastAPI
- Python
- Uvicorn
- JWT (JSON Web Token)
- bcrypt
- Pydantic
- Swagger UI

---

