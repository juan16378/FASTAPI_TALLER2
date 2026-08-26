from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.productos,
        name="productos"
    ),

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    path(
        "crear-pedido/",
        views.crear_pedido,
        name="crear_pedido"
    ),

]