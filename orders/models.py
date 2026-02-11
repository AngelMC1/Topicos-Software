from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=120)
    brand = models.CharField(max_length=80, blank=True, default="")
    sku = models.CharField(max_length=60, blank=True, default="")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ("CREATED", "CREATED"),
        ("PAID", "PAID"),
        ("CANCELLED", "CANCELLED"),
    ]

    customer_email = models.EmailField()
    city = models.CharField(max_length=80)
    address_line = models.CharField(max_length=200)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    import_fee = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="CREATED")
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
