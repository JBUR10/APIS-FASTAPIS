from fastapi import FastAPI
from routers import productos, categorias, empleados, proveedores
 
app = FastAPI(title="API de la Tienda")
 
app.include_router(productos.router)
app.include_router(categorias.router)
app.include_router(empleados.router)
app.include_router(proveedores.router)
 
@app.get("/", tags=["Inicio"])
def inicio():
	return {"mensaje": "API de la Tienda funcionando. Visita /docs"}
