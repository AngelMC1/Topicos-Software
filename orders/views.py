import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .services import OrderService, CreateOrderRequest

@method_decorator(csrf_exempt, name="dispatch")
class PlaceOrderView(View):
    def post(self, request):
        p=json.loads(request.body or b"{}")
        o=OrderService().create_order(CreateOrderRequest(p["customer_email"], p["items"], p["address"]))
        return JsonResponse({"order_id": o.id, "status": o.status})
