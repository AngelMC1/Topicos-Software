from django.urls import path
from .views import (
    ProductListAPIView,
    OrderCreateAPIView,
    OrderDetailAPIView,
    ExchangeRateAPIView,
    SystemStatusAPIView,
    AlliedServiceView,
)

urlpatterns = [
    path("products/", ProductListAPIView.as_view(), name="product-list"),
    path("checkout/place-order/", OrderCreateAPIView.as_view(), name="place-order"),
    path("orders/<int:order_id>/", OrderDetailAPIView.as_view(), name="order-detail"),
    path("exchange-rate/", ExchangeRateAPIView.as_view(), name="exchange-rate"),
    path("status/", SystemStatusAPIView.as_view(), name="system-status"),
    path("allied/", AlliedServiceView.as_view(), name="allied-service"),
]