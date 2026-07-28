from fastapi import FastAPI
from routers import productos, categorias
 
app = FastAPI(title="API de la Tienda")
 
app.include_router(productos.router)
app.include_router(categorias.router)
 
@app.get("/", tags=["Inicio"])
def inicio():
	return {"mensaje": "API de la Tienda funcionando. Visita /docs"}
