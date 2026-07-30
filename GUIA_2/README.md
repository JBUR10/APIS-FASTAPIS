# API CRUD con FastAPI

Este proyecto consiste en una API REST desarrollada con **FastAPI** para gestionar productos y categorías mediante operaciones CRUD (Crear, Leer, Actualizar y Eliminar).

## Requisitos

- Python 3.10 o superior
- FastAPI
- Uvicorn

## Instalación

Instala las dependencias con el siguiente comando:

```bash
pip install fastapi uvicorn
```

## Ejecución

Inicia el servidor con:

```bash
uvicorn main:app --reload
```

La aplicación estará disponible en:

- http://127.0.0.1:8000

## Documentación

FastAPI genera automáticamente la documentación de la API.

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Endpoints

### Productos

- `GET /productos`
- `GET /productos/{id}`
- `POST /productos`
- `PUT /productos/{id}`
- `DELETE /productos/{id}`

### Categorías

- `GET /categorias`
- `GET /categorias/{id}`
- `POST /categorias`
- `PUT /categorias/{id}`
- `DELETE /categorias/{id}`

### Empleados

- `GET /empleados`
- `GET /empleados/{id}`
- `POST /empleados`
- `PUT /empleados/{id}`
- `DELETE /empleados/{id}`

### Proveedores

- `GET /proveedores`
- `GET /proveedores/{id}`
- `POST /proveedores`
- `PUT /proveedores/{id}`
- `DELETE /proveedores/{id}`



