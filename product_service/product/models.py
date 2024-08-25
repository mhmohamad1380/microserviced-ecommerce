from django.db import models
from .validators import validate_product_details

class Category(models.Model):
    title = models.CharField(max_length=32, blank=False, null=True)

    def __str__(self) -> str:
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=128, blank=False, null=True)
    category = models.ForeignKey(to="Category", null=True, blank=False, on_delete=models.CASCADE)
    seller = models.PositiveIntegerField(null=True, blank=False)
    details = models.JSONField(validators=[validate_product_details])

    def __str__(self) -> str:
        return self.title
    
