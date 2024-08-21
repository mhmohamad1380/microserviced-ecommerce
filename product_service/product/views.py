from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .permissions import IsAuthenticatedCustom
from .serializers import serializer_product
from .paginations import ProductPagination
from .models import Product
from django.db.models import F
from .utils import get_user_token

class ProductAPIView(APIView):
    permission_classes = [IsAuthenticatedCustom]
    pagination_class = ProductPagination
    required_fields = ['title', "category", "details"]

    def get(self, request):
        products = Product.objects.select_related("category").annotate(
            category_title=F("category__title")
        )

        paginate = self.pagination_class()
        serialize = serializer_product(products, many=True)
        paginate_queryset = paginate.paginate_queryset(serialize, request)
        return paginate.get_paginated_response(paginate_queryset)
    
    def post(self, request):
        if not all(field in request.data for field in self.required_fields):
            return Response({"message": f"Please provide all required fields: {self.required_fields}"})
        
        user_id = get_user_token(request)
        if "error" in user_id:
            return Response({"error": user_id['error']})
        
        product = Product.objects.create(
            title=self.request.data.get("title"),
            category_id=self.request.data.get("category"),
            details=self.request.data.get("details"),
            seller=user_id['pk']
        )
        return Response({"message": "the Product has been created successfully!"}, status=status.HTTP_200_OK)