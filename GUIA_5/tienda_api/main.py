from fastapi import FastAPI
from routers import auth, productos, categorias, proveedores, empleados
from database import db

app = FastAPI(title="API de la Tienda")

conexion = db.crearTablas()

app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(categorias.router)
app.include_router(proveedores.router)
app.include_router(empleados.router)


@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "API de la Tienda funcionando. Visita /docs"}
