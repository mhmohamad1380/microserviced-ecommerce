from rest_framework.views import APIView
from .permissions import IsAuthenticatedCustom
from rest_framework.response import Response
import requests
from rest_framework import status
from django.conf import settings
from .models import Cart
from .utils import get_user_token
from .paginations import CartPagination
from django.db.models import Q

products_service_address = settings.PRODUCT_SERVICE_ADDRESS


class CartAPIView(APIView):
    permission_classes = [IsAuthenticatedCustom]
    required_fields = ["product", "detail-index", "count"]
    pagination_class = CartPagination

    def get(self, request):
        if not "cart-id" in request.headers:
            carts = Cart.objects.filter(user=get_user_token(request)['pk']).values("user", "product", "detail_index", "count", "pk")

            paginate = self.pagination_class()
            paginate_queryset = paginate.paginate_queryset(carts, request)
            data = [
                {
                    "pk": cart['pk'],
                    "user": cart['user'],
                    "product": cart['product'],
                    "detail_index": cart['detail_index']
                } for cart in paginate_queryset
            ]
            return paginate.get_paginated_response(data)
        
        cart_id = request.headers['cart-id']
        cart = Cart.objects.filter(Q(pk=cart_id)).values("user", "product", "detail_index", "count", "pk")
        if not cart.exists():
            return Response({"message": "this Cart does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        cart = cart.first()
        product = requests.get(f"{products_service_address}/api/products/", headers={"product-id": cart['product']})

        return Response(
            {
                "pk": cart['pk'],
                "product_pk": product['pk'],
                "title": product['title'],
                "category": product['category'],
                "seller": product['seller'],
                "detail": product['details'][cart['detail_index']]
            }, status=status.HTTP_200_OK
        )

    def post(self, request):
        if not all(field in request.headers for field in self.required_fields):
            return Response({"message": f"Please Provide all required fields: {self.required_fields}"})
        
        product = request.headers.get('product')
        detail_index = request.headers.get('detail-index')
        count = request.headers.get('count')

        validate_product = requests.post(f"{products_service_address}/api/product/validate/", headers={"product-id": product, "detail-index": detail_index, "count": count})
        if validate_product.status_code != 200:
            return Response({"message": "Something went Wrong!"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_id = get_user_token(request)
        user_id = user_id['pk']

        Cart.objects.create(product=product, user=user_id, detail_index=detail_index, count=count)
        return Response({"message": "the Cart has been created successfully!"}, status=status.HTTP_200_OK)
