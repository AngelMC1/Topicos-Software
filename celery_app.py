import os
from celery import Celery

# URL del Broker apuntando al servicio RabbitMQ del Stack
BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://guest:guest@rabbitmq:5672//')

app = Celery('ropium', broker=BROKER_URL)

@app.task
def notificar_compra_exitosa(email, orden_id):
    # Lógica simulada de envío de correo tras una compra
    return f"Notificación enviada a {email} para la orden {orden_id}"