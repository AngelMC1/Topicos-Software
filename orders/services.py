from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Any, List, Optional

from orders.models import Product
from .domain.builders import OrderBuilder, ItemInput
from .infra.factories import NotifierFactory
from .infra.notifier import OrderConfirmationData, Notifier


@dataclass
class CreateOrderRequest:
    customer_email: str
    items: List[Dict[str, Any]]   # [{"product_id": 1, "qty": 2}, ...]
    address: Dict[str, Any]       # {"city": "...", "address_line": "..."}


class OrderService:
    def __init__(self, notifier: Optional[Notifier] = None):
        # DI: si te inyectan uno (tests), lo usa; si no, usa Factory.
        self.notifier = notifier or NotifierFactory.create()

    @staticmethod
    def _money(x: Decimal) -> Decimal:
        """Asegura 2 decimales (DecimalField decimal_places=2) para que full_clean() no falle."""
        return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def create_order(self, req: CreateOrderRequest):
        # 1) Normaliza items
        items_input = [ItemInput(int(i["product_id"]), int(i["qty"])) for i in req.items]

        # 2) Trae productos y valida existencia/activos
        product_ids = [it.product_id for it in items_input]
        products = {
            p.id: p for p in Product.objects.filter(id__in=product_ids, is_active=True)
        }

        # 3) Calcula subtotal (regla de negocio)
        subtotal = Decimal("0")
        for it in items_input:
            product = products.get(it.product_id)
            if not product:
                raise ValueError(f"Producto {it.product_id} no existe o no está activo.")
            if it.qty <= 0:
                raise ValueError("Cantidad inválida (debe ser > 0).")
            subtotal += product.price * it.qty

        subtotal = self._money(subtotal)

        # 4) Fees/Shipping (reglas simples para el taller)
        import_fee = self._money(subtotal * Decimal("0.08"))   # 8% importación bajo pedido
        shipping = self._money(Decimal("15000.00"))            # envío fijo
        total = self._money(subtotal + import_fee + shipping)

        pricing = {
            "subtotal": subtotal,
            "import_fee": import_fee,
            "shipping": shipping,
            "total": total,
        }

        # 5) Orquesta Builder (validación antes de guardar está en el builder)
        order = (
            OrderBuilder()
            .for_customer(req.customer_email)
            .with_items(items_input)
            .ship_to(req.address)
            .with_pricing(pricing)
            .build_and_save()
        )

        # 6) Notificación (Factory MOCK/REAL) - evidencia del taller
        self.notifier.send_order_confirmation(
            OrderConfirmationData(
                order_id=order.id,
                user_email=order.customer_email,
                total=str(order.total),
            )
        )
        return order
