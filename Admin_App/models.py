from django.db import models

# Create your models here.

# ------------------------------------------------- Category ---------------------------------------------------------------------- #
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_image', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
    
