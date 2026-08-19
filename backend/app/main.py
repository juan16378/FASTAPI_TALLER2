from fastapi import FastAPI

from app.routes.productos import router as productos_router
from app.routes.pedidos import router as pedidos_router


app = FastAPI(
    title="API Tienda",
    description="API REST para gestión de productos y pedidos",
    version="1.0.0"
)


app.include_router(productos_router)
app.include_router(pedidos_router)


@app.get("/")
def inicio():
    return {
        "mensaje": "API funcionando correctamente"
    }