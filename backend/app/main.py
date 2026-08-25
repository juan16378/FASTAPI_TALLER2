from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.productos import router as productos_router
from app.routes.pedidos import router as pedidos_router


app = FastAPI(
    title="API Tienda",
    description="API REST para gestión de productos y pedidos",
    version="1.0.0"
)


# ==========================
# CORS
# ==========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8001",
        "http://localhost:8001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================
# RUTAS
# ==========================

app.include_router(productos_router)
app.include_router(pedidos_router)


# ==========================
# INICIO
# ==========================

@app.get("/")
def inicio():
    return {
        "mensaje": "API funcionando correctamente"
    }