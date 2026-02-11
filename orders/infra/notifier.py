from dataclasses import dataclass
from django.core.mail import send_mail

@dataclass
class OrderConfirmationData:
    order_id: int
    user_email: str
    total: str

class Notifier:
    def send_order_confirmation(self, data: OrderConfirmationData) -> None:
        raise NotImplementedError

class ConsoleNotifier(Notifier):  # MOCK
    def send_order_confirmation(self, data: OrderConfirmationData) -> None:
        print(f"[MOCK] Pedido #{data.order_id} -> {data.user_email} | Total: {data.total}")

class EmailNotifier(Notifier):  # REAL
    def send_order_confirmation(self, data: OrderConfirmationData) -> None:
        send_mail(
            subject=f"Ropium Casual: Confirmación pedido #{data.order_id}",
            message=f"Tu pedido fue creado correctamente. Total: {data.total}",
            from_email=None,
            recipient_list=[data.user_email],
            fail_silently=False,
        )
