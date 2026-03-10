from django.urls import path
from .views import ProductListAPIView, OrderCreateAPIView, OrderDetailAPIView

urlpatterns = [
    path("products/", ProductListAPIView.as_view(), name="product-list"),
    path("orders/", OrderCreateAPIView.as_view(), name="order-create"),
    path("orders/<int:order_id>/", OrderDetailAPIView.as_view(), name="order-detail"),
]