import os
from flask import Flask, request, jsonify
from celery import Celery

app = Flask(__name__)

# Mismo broker Redis que usa el worker de Django — permite disparar tareas desde Flask
_broker = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
celery_client = Celery(broker=_broker)


@app.route("/api/v2/checkout/place-order/", methods=["POST"])
def create_order():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"detail": "No se recibió JSON válido."}), 400

        customer_email = data.get("customer_email")
        items = data.get("items")
        address = data.get("address")

        if not customer_email:
            return jsonify({"detail": "customer_email es obligatorio."}), 400

        if not items or not isinstance(items, list):
            return jsonify({"detail": "items es obligatorio y debe ser una lista."}), 400

        if not address or not isinstance(address, dict):
            return jsonify({"detail": "address es obligatorio y debe ser un objeto."}), 400

        subtotal = 0
        for item in items:
            qty = item.get("qty", 0)
            if qty <= 0:
                return jsonify({"detail": "Cantidad inválida. Debe ser mayor que 0."}), 400
            subtotal += 100000 * qty

        import_fee = round(subtotal * 0.08, 2)
        shipping = 15000.00
        total = round(subtotal + import_fee + shipping, 2)

        # Dispara tarea asíncrona al worker de Celery (Django) sin bloquear la respuesta
        try:
            celery_client.send_task(
                "orders.notify_order_created",
                args=[None, customer_email, str(total)],
            )
        except Exception:
            pass  # No falla el checkout si Celery no está disponible

        return jsonify({
            "message": "Pedido procesado en microservicio Flask",
            "customer_email": customer_email,
            "address": address,
            "items": items,
            "pricing": {
                "subtotal": subtotal,
                "import_fee": import_fee,
                "shipping": shipping,
                "total": total,
            },
        }), 201

    except Exception as e:
        return jsonify({
            "detail": "Error interno al procesar el pedido.",
            "error": str(e),
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
