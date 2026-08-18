from fastapi import FastAPI
from app.database import client, db

app = FastAPI(
    title="API Tienda",
    description="Backend de la tienda",
    version="1.0.0"
)


@app.get("/")
def inicio():
    return {
        "mensaje": "API funcionando correctamente"
    }


@app.get("/conexion")
def comprobar_conexion():
    try:
        client.admin.command("ping")

        return {
            "mensaje": "Conexión con MongoDB exitosa",
            "base_datos": db.name
        }

    except Exception as e:
        return {
            "mensaje": "Error de conexión",
            "error": str(e)
        }