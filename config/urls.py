from django.contrib import admin
from django.urls import path, include
from orders.views import home_page, catalog_page, cart_page, checkout_page

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", home_page, name="home"),
    path("catalogo/", catalog_page, name="catalogo"),
    path("carrito/", cart_page, name="carrito"),
    path("checkout/", checkout_page, name="checkout"),

    path("api/", include("orders.urls")),
]