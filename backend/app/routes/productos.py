from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.database import productos_collection
from app.models.producto import Producto


router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


def producto_schema(producto):
    return {
        "id": str(producto["_id"]),
        "nombre": producto["nombre"],
        "descripcion": producto["descripcion"],
        "precio": producto["precio"],
        "categoria": producto["categoria"],
        "stock": producto["stock"]
    }


@router.post("/")
async def crear_producto(producto: Producto):
    resultado = await productos_collection.insert_one(
        producto.model_dump()
    )

    nuevo_producto = await productos_collection.find_one(
        {"_id": resultado.inserted_id}
    )

    return producto_schema(nuevo_producto)


@router.get("/")
async def obtener_productos():
    productos = productos_collection.find()

    return [
        producto_schema(producto)
        async for producto in productos
    ]


@router.get("/{producto_id}")
async def obtener_producto(producto_id: str):

    try:
        object_id = ObjectId(producto_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="ID de producto inválido"
        )

    producto = await productos_collection.find_one(
        {"_id": object_id}
    )

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return producto_schema(producto)


@router.put("/{producto_id}")
async def actualizar_producto(
    producto_id: str,
    producto: Producto
):

    try:
        object_id = ObjectId(producto_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="ID de producto inválido"
        )

    resultado = await productos_collection.update_one(
        {"_id": object_id},
        {"$set": producto.model_dump()}
    )

    if resultado.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    producto_actualizado = await productos_collection.find_one(
        {"_id": object_id}
    )

    return producto_schema(producto_actualizado)


@router.delete("/{producto_id}")
async def eliminar_producto(producto_id: str):

    try:
        object_id = ObjectId(producto_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="ID de producto inválido"
        )

    resultado = await productos_collection.delete_one(
        {"_id": object_id}
    )

    if resultado.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return {
        "mensaje": "Producto eliminado correctamente"
    }