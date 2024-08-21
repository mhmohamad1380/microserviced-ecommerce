from .models import Product

def serializer_product(product_instance: Product, many: bool=False): # I did not use default serializers because they are slower than these normal function I wrote!
    if many:
        return [
            {
                "pk": product['pk'],
                "title": product['title'],
                "category": {
                    "pk": product['category_pk'],
                    "title": product['category_title'],
                },
                "seller": product['seller'],
                "details": product['details']
            } for product in product_instance
        ] 
    
    return {
                "pk": product_instance['pk'],
                "title": product_instance['title'],
                "category": {
                    "pk": product_instance['category_pk'],
                    "title": product_instance['category_title'],
                },
                "seller": product_instance['seller'],
                "details": product_instance['details']
            }