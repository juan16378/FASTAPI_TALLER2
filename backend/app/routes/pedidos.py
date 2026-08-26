from fastapi import APIRouter, HTTPException

from app.database import pedidos_collection
from app.database import productos_collection

from app.models.pedido import Pedido


router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


@router.post("/")
async def crear_pedido(pedido: Pedido):

    # ==========================================
    # 1. VALIDAR Y DESCONTAR STOCK
    # ==========================================

    for producto_pedido in pedido.productos:

        producto_id = producto_pedido.producto_id
        cantidad = producto_pedido.cantidad

        # Buscar producto
        from bson import ObjectId

        try:
            object_id = ObjectId(producto_id)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail=f"ID de producto inválido: {producto_id}"
            )

        producto = await productos_collection.find_one(
            {
                "_id": object_id
            }
        )

        # Producto no existe
        if not producto:

            raise HTTPException(
                status_code=404,
                detail=(
                    f"El producto con ID "
                    f"{producto_id} no existe."
                )
            )

        stock_actual = producto.get(
            "stock",
            0
        )

        # ==========================================
        # 2. COMPROBAR STOCK
        # ==========================================

        if stock_actual < cantidad:

            raise HTTPException(
                status_code=400,
                detail=(
                    f"No hay suficiente stock de "
                    f"'{producto.get('nombre', 'producto')}'. "
                    f"Disponible: {stock_actual}. "
                    f"Solicitado: {cantidad}."
                )
            )


    # ==========================================
    # 3. DESCONTAR STOCK
    # ==========================================

    for producto_pedido in pedido.productos:

        producto_id = producto_pedido.producto_id
        cantidad = producto_pedido.cantidad

        from bson import ObjectId

        object_id = ObjectId(producto_id)

        resultado = await productos_collection.update_one(

            {
                "_id": object_id,

                # Esto evita descontar si el stock
                # cambió mientras se procesaba la compra
                "stock": {
                    "$gte": cantidad
                }
            },

            {
                "$inc": {
                    "stock": -cantidad
                }
            }

        )

        # No se pudo actualizar
        if resultado.modified_count == 0:

            raise HTTPException(

                status_code=400,

                detail=(
                    "El stock cambió mientras "
                    "se procesaba la compra. "
                    "Intenta nuevamente."
                )

            )


    # ==========================================
    # 4. REGISTRAR PEDIDO
    # ==========================================

    resultado = await pedidos_collection.insert_one(

        pedido.model_dump()

    )


    # ==========================================
    # 5. RESPUESTA
    # ==========================================

    return {

        "mensaje":
            "Pedido registrado correctamente",

        "id":
            str(resultado.inserted_id)

    }


@router.get("/")
async def obtener_pedidos():

    pedidos = pedidos_collection.find()

    resultado = []


    async for pedido in pedidos:

        resultado.append({

            "id":
                str(pedido["_id"]),

            "nombre_completo":
                pedido.get(
                    "nombre_completo",
                    ""
                ),

            "cedula":
                pedido.get(
                    "cedula",
                    ""
                ),

            "celular":
                pedido.get(
                    "celular",
                    ""
                ),

            "correo":
                pedido.get(
                    "correo",
                    ""
                ),

            "direccion":
                pedido.get(
                    "direccion",
                    ""
                ),

            "ciudad":
                pedido.get(
                    "ciudad",
                    ""
                ),

            "notas":
                pedido.get(
                    "notas",
                    ""
                ),

            "productos":
                pedido.get(
                    "productos",
                    []
                ),

            "total":
                pedido.get(
                    "total",
                    0
                )

        })


    return resultado