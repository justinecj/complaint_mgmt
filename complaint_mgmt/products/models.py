from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name