from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Order
from .serializers import (
    ProductSerializer,
    CreateOrderInputSerializer,
    OrderOutputSerializer,
)
from .services import OrderService, CreateOrderRequest
from .infra.adapters.exchange_rate_adapter import ExchangeRateAdapter
from .infra.adapters.allied_service_adapter import AlliedServiceAdapter


class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderCreateAPIView(APIView):
    def post(self, request):
        serializer = CreateOrderInputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        try:
            order = OrderService().create_order(
                CreateOrderRequest(
                    customer_email=data["customer_email"],
                    items=data["items"],
                    address=data["address"],
                )
            )
            output = OrderOutputSerializer(order)
            return Response(output.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)

        except Exception:
            return Response(
                {"detail": "Error interno al crear el pedido."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class OrderDetailAPIView(APIView):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"detail": "Pedido no encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = OrderOutputSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SystemStatusAPIView(APIView):
    """
    Endpoint público que expone información del sistema Ropium.
    Pensado para ser consumido por el equipo aliado (requisito de integración).
    """
    def get(self, request):
        product_count = Product.objects.filter(is_active=True).count()
        order_count = Order.objects.count()
        return Response({
            "service": "ropium-monolito",
            "version": "2.0.0",
            "status": "healthy",
            "timestamp": timezone.now().isoformat(),
            "data": {
                "active_products": product_count,
                "total_orders": order_count,
                "currency": "COP",
                "marketplace": "Ropium Casual — Importados",
                "endpoints": {
                    "products": "/api/products/",
                    "place_order": "/api/v2/checkout/place-order/",
                    "order_detail": "/api/orders/<id>/",
                    "exchange_rate": "/api/exchange-rate/",
                    "status": "/api/status/",
                },
            },
        }, status=status.HTTP_200_OK)


class ExchangeRateAPIView(APIView):
    """
    Expone el tipo de cambio USD → COP usando el Patrón Adapter (DIP).
    El cliente (frontend o equipo aliado) consulta este endpoint para mostrar precios en USD.
    """
    def get(self, request):
        adapter = ExchangeRateAdapter()
        rate = adapter.get_usd_to_cop()
        return Response({
            "base": "USD",
            "target": "COP",
            "rate": float(rate),
            "source": "open.er-api.com",
        }, status=status.HTTP_200_OK)


class AlliedServiceView(APIView):
    """
    Consume el servicio del equipo aliado vía AlliedServiceAdapter (Patrón Adapter, DIP).
    La URL se configura con la variable de entorno ALLIED_SERVICE_URL.
    """
    def get(self, request):
        adapter = AlliedServiceAdapter()
        result = adapter.get_status()
        http_status = status.HTTP_200_OK if result.get("available") else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response(result, status=http_status)


def home_page(request):
    return render(request, "frontend/home.html")


def catalog_page(request):
    return render(request, "frontend/catalog.html")


def cart_page(request):
    return render(request, "frontend/cart.html")


def checkout_page(request):
    return render(request, "frontend/checkout.html")