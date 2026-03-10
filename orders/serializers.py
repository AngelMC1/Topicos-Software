from rest_framework import serializers
from .models import Product, Order, OrderItem


class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    qty = serializers.IntegerField(min_value=1)


class AddressInputSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=80)
    address_line = serializers.CharField(max_length=200)


class CreateOrderInputSerializer(serializers.Serializer):
    customer_email = serializers.EmailField()
    items = OrderItemInputSerializer(many=True)
    address = AddressInputSerializer()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "brand", "sku", "price", "is_active"]


class OrderItemOutputSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["product", "product_name", "qty", "unit_price"]


class OrderOutputSerializer(serializers.ModelSerializer):
    items = OrderItemOutputSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_email",
            "city",
            "address_line",
            "subtotal",
            "import_fee",
            "shipping_cost",
            "total",
            "status",
            "created_at",
            "items",
        ]