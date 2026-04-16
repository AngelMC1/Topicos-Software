from django.shortcuts import render
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


def home_page(request):
    return render(request, "frontend/home.html")


def catalog_page(request):
    return render(request, "frontend/catalog.html")


def cart_page(request):
    return render(request, "frontend/cart.html")


def checkout_page(request):
    return render(request, "frontend/checkout.html")