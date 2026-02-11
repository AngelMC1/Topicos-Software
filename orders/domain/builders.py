from dataclasses import dataclass
from decimal import Decimal
from typing import List, Dict, Any
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from orders.models import Order, OrderItem, Product

@dataclass
class ItemInput:
    product_id: int
    qty: int

class OrderBuilder:
    def __init__(self):
        self._email = None
        self._items: List[ItemInput] = []
        self._address: Dict[str, Any] = {}
        self._pricing: Dict[str, Decimal] = {}

    # Fluent Interface
    def for_customer(self, email: str):
        self._email = email
        return self

    def with_items(self, items: List[ItemInput]):
        self._items = items
        return self

    def ship_to(self, address: Dict[str, Any]):
        self._address = address
        return self

    def with_pricing(self, pricing: Dict[str, Decimal]):
        self._pricing = pricing
        return self

    def _validate(self):
        if not self._email:
            raise ValidationError("customer_email requerido.")
        validate_email(self._email)

        if not self._items:
            raise ValidationError("Carrito vacío.")
        for it in self._items:
            if it.qty <= 0:
                raise ValidationError("Cantidad inválida (debe ser > 0).")

        if "city" not in self._address or "address_line" not in self._address:
            raise ValidationError("Dirección incompleta.")

        if self._pricing.get("total", Decimal("0")) <= 0:
            raise ValidationError("Total inválido.")

    @transaction.atomic
    def build_and_save(self) -> Order:
        self._validate()

        order = Order(
            customer_email=self._email,
            city=self._address["city"],
            address_line=self._address["address_line"],
            subtotal=self._pricing["subtotal"],
            import_fee=self._pricing["import_fee"],
            shipping_cost=self._pricing["shipping"],
            total=self._pricing["total"],
            status="CREATED",
        )

        # Validez antes de guardar (requisito del PDF)
        order.full_clean()
        order.save()

        for it in self._items:
            product = Product.objects.select_for_update().get(id=it.product_id, is_active=True)
            OrderItem.objects.create(
                order=order,
                product=product,
                qty=it.qty,
                unit_price=product.price,
            )

        return order
