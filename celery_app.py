import os
from celery import Celery

# Usando Redis como broker en lugar de RabbitMQ
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('ropium')
app.conf.broker_url = 'redis://redis:6379/0'
app.autodiscover_tasks()

@app.task
def notificar_compra_exitosa(email, orden_id):
    return f"Notificación enviada a {email} para la orden {orden_id}"