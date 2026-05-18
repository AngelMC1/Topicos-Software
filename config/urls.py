from django.contrib import admin
from django.urls import path, include
from django.views.i18n import JavaScriptCatalog
from orders.views import home_page, catalog_page, cart_page, checkout_page

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),

    path("", home_page, name="home"),
    path("catalogo/", catalog_page, name="catalogo"),
    path("carrito/", cart_page, name="carrito"),
    path("checkout/", checkout_page, name="checkout"),

    path("api/", include("orders.urls")),
]