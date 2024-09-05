from .models import Product
import json

def serializer_product(product_instance: Product, many: bool=False): # I did not use default serializers because they are slower than these normal function I wrote!
    if many:
        return [
            {
                "pk": product['pk'],
                "title": product['title'],
                "category": {
                    "pk": product['category_id'],
                    "title": product['category_title'],
                },
                "seller": product['seller'],
                "details": json.loads(product['details'])
            } for product in product_instance
        ] 
    
    return {
                "pk": product_instance['pk'],
                "title": product_instance['title'],
                "category": {
                    "pk": product_instance['category_id'],
                    "title": product_instance['category_title'],
                },
                "seller": product_instance['seller'],
                "details": json.loads(product_instance['details'])
            }