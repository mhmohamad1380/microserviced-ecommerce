from django.urls import path
from .views import ProductAPIView, validate_product

urlpatterns = [
    path("products/", ProductAPIView.as_view(), name="products"),
    path("product/validate/", validate_product, name="validate-product"),
]