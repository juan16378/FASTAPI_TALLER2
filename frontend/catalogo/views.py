import json
import requests

from django.shortcuts import render, redirect


API_URL = "https://fastapi-taller2-kqhc.onrender.com"


def productos(request):

    productos_data = []
    error = None

    try:
        url = f"{API_URL}/productos/"

        print("================================")
        print("URL API:", url)
        print("================================")

        respuesta = requests.get(
            url,
            timeout=20
        )

        print("STATUS:", respuesta.status_code)
        print("RESPUESTA:", respuesta.text)

        if respuesta.status_code == 200:
            productos_data = respuesta.json()
        else:
            error = (
                f"La API respondió con código "
                f"{respuesta.status_code}: {respuesta.text}"
            )

    except requests.exceptions.Timeout:
        error = "La API de Render tardó demasiado en responder."

    except requests.exceptions.ConnectionError as e:
        error = f"Error de conexión con Render: {e}"

    except requests.exceptions.RequestException as e:
        error = f"Error HTTP al conectar con la API: {e}"

    except Exception as e:
        error = f"Error inesperado: {e}"

    return render(
        request,
        "catalogo/productos.html",
        {
            "productos": productos_data,
            "error": error,
        }
    )


def checkout(request):

    return render(
        request,
        "catalogo/checkout.html"
    )


def crear_pedido(request):

    # -----------------------------------------
    # SOLO PERMITIR POST
    # -----------------------------------------

    if request.method != "POST":

        return redirect("checkout")


    try:

        # -----------------------------------------
        # DATOS DEL CLIENTE
        # -----------------------------------------

        nombre_completo = request.POST.get(
            "nombre_completo",
            ""
        ).strip()

        cedula = request.POST.get(
            "cedula",
            ""
        ).strip()

        celular = request.POST.get(
            "celular",
            ""
        ).strip()

        correo = request.POST.get(
            "correo",
            ""
        ).strip()

        direccion = request.POST.get(
            "direccion",
            ""
        ).strip()

        ciudad = request.POST.get(
            "ciudad",
            ""
        ).strip()

        notas = request.POST.get(
            "notas",
            ""
        ).strip()


        # -----------------------------------------
        # PRODUCTOS
        # -----------------------------------------

        productos_json = request.POST.get(
            "productos",
            "[]"
        )


        productos = json.loads(
            productos_json
        )


        # -----------------------------------------
        # TOTAL
        # -----------------------------------------

        total = float(
            request.POST.get(
                "total",
                "0"
            )
        )


        # -----------------------------------------
        # VALIDACIONES
        # -----------------------------------------

        if not nombre_completo:

            return render(
                request,
                "catalogo/checkout.html",
                {
                    "error":
                        "El nombre completo es obligatorio."
                }
            )


        if not cedula:

            return render(
                request,
                "catalogo/checkout.html",
                {
                    "error":
                        "La cédula es obligatoria."
                }
            )


        if not celular:

            return render(
                request,
                "catalogo/checkout.html",
                {
                    "error":
                        "El número de celular es obligatorio."
                }
            )


        if not correo:

            return render(
                request,
                "catalogo/checkout.html",
                {
                    "error":
                        "El correo electrónico es obligatorio."
                }
            )


        if not direccion:

            return render(
                request,
                "catalogo/checkout.html",
                {
                    "error":
                        "La dirección es obligatoria."
                }
            )


        if not ciudad:

            return render(
                request,
                "catalogo/checkout.html",
                {
                    "error":
                        "La ciudad es obligatoria."
                }
            )


        if not productos:

            return render(
                request,
                "catalogo/checkout.html",
                {
                    "error":
                        "El carrito está vacío."
                }
            )


        if total <= 0:

            return render(
                request,
                "catalogo/checkout.html",
                {
                    "error":
                        "El total del pedido no es válido."
                }
            )


        # -----------------------------------------
        # CONSTRUIR PEDIDO PARA FASTAPI
        # -----------------------------------------

        pedido = {

            "nombre_completo":
                nombre_completo,

            "cedula":
                cedula,

            "celular":
                celular,

            "correo":
                correo,

            "direccion":
                direccion,

            "ciudad":
                ciudad,

            "notas":
                notas,

            "productos":
                productos,

            "total":
                total

        }


        print("\n==============================")
        print("ENVIANDO PEDIDO A FASTAPI")
        print("==============================")
        print(pedido)


        # -----------------------------------------
        # ENVIAR A FASTAPI
        # -----------------------------------------

        respuesta = requests.post(

            f"{API_URL}/pedidos/",

            json=pedido,

            timeout=10

        )


        print("\nRESPUESTA FASTAPI")
        print("Status:", respuesta.status_code)
        print("Body:", respuesta.text)


        # -----------------------------------------
        # SI FASTAPI RECHAZA EL PEDIDO
        # -----------------------------------------

        if respuesta.status_code not in [200, 201]:

            try:

                detalle = respuesta.json()

            except ValueError:

                detalle = respuesta.text


            return render(

                request,

                "catalogo/checkout.html",

                {

                    "error":
                        f"FastAPI rechazó el pedido: {detalle}"

                }

            )


        # -----------------------------------------
        # OBTENER RESPUESTA
        # -----------------------------------------

        resultado = respuesta.json()


        pedido_id = resultado.get("id")


        if not pedido_id:

            return render(

                request,

                "catalogo/checkout.html",

                {

                    "error":
                        "FastAPI registró el pedido "
                        "pero no devolvió el ID."

                }

            )


        # -----------------------------------------
        # PEDIDO EXITOSO
        # -----------------------------------------

        return render(

            request,

            "catalogo/pedido_exitoso.html",

            {

                "pedido": {

                    "id":
                        pedido_id,

                    "total":
                        total,

                    "nombre_completo":
                        nombre_completo

                }

            }

        )


    # -----------------------------------------
    # ERRORES
    # -----------------------------------------

    except json.JSONDecodeError:

        return render(

            request,

            "catalogo/checkout.html",

            {

                "error":
                    "Los productos enviados "
                    "no tienen un formato válido."

            }

        )


    except requests.exceptions.ConnectionError:

        return render(

            request,

            "catalogo/checkout.html",

            {

                "error":
                    "No se pudo conectar con FastAPI. "
                    "Verifica que Uvicorn esté ejecutándose "
                    "en el puerto 8000."

            }

        )


    except requests.exceptions.Timeout:

        return render(

            request,

            "catalogo/checkout.html",

            {

                "error":
                    "FastAPI tardó demasiado en responder."

            }

        )


    except Exception as error:

        print("\nERROR CREANDO PEDIDO:")
        print(error)

        return render(

            request,

            "catalogo/checkout.html",

            {

                "error":
                    f"Ocurrió un error al procesar "
                    f"el pedido: {error}"

            }

        )