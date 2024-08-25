from rest_framework.views import APIView
from product_service.product.permissions import IsAuthenticatedCustom
from rest_framework.response import Response
import requests
from rest_framework import status
from django.conf import settings
from .models import Cart
from product_service.product.utils import get_user_token

products_service_address = settings.PRODUCT_SERVICE_ADDRESS


class CartAPIView(APIView):
    permission_classes = [IsAuthenticatedCustom]
    required_fields = ["product", "detail-index", "count"]

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
