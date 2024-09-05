from django.urls import path
from .views import CartAPIView

urlpatterns = [
    path("carts/", CartAPIView.as_view(), name="carts")
]