from django.db import models
from Admin_App.models import Product
# Create your models here.

class Cart(models.Model):
    user_session_key = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart ({self.user_session_key})"

class CartItem(models.Model):
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=50)
    whatsapp_number = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order ({self.id})"