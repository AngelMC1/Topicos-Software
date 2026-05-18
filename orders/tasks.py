from celery import shared_task


@shared_task(name="orders.notify_order_created", bind=True, max_retries=3)
def notify_order_created(self, order_id: int, email: str, total: str):
    """
    Tarea asíncrona: simula el envío de confirmación de compra.
    Se ejecuta en el worker de Celery, no en el proceso principal de Django.
    """
    try:
        print(f"[Celery] Orden #{order_id} confirmada → {email} (total: {total})")
        return {"sent": True, "order_id": order_id, "email": email}
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
