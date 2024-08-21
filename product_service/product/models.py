from django.db import models
from django.core.exceptions import ValidationError

def validate_product_details(value):
    """
    Validate that each item in the list is a dictionary with the required keys.
    """
    required_keys = {'price', 'size', 'color', 'count'}
    
    if not isinstance(value, list):
        raise ValidationError("The field should be a list of dictionaries.")
    
    for item in value:
        if not isinstance(item, dict):
            raise ValidationError("Each item must be a dictionary.")
        if not required_keys.issubset(item.keys()):
            raise ValidationError(f"Each dictionary must contain the keys: {required_keys}")


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
    
