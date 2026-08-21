import requests
from django.shortcuts import render

API_URL = "http://127.0.0.1:8000/productos/"


def lista_productos(request):
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        productos = response.json()
        error = None
    except requests.exceptions.RequestException as e:
        productos = []
        error = f"No se pudo conectar con la API: {e}"

    return render(request, "catalogo/lista_productos.html", {
        "productos": productos,
        "error": error
    })