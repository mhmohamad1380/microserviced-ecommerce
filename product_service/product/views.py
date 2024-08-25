from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .permissions import IsAuthenticatedCustom
from .serializers import serializer_product
from .paginations import ProductPagination
from .models import Product
from django.db.models import F, Q
from .utils import get_user_token

class ProductAPIView(APIView):
    permission_classes = [IsAuthenticatedCustom]
    pagination_class = ProductPagination
    required_fields = ['title', "category", "details"]

    def get(self, request):
        products = Product.objects.select_related("category").annotate(
            category_title=F("category__title")
        ).values("pk", "title", "category_id", "category_title", "seller", "details")

        paginate = self.pagination_class()
        serialize = serializer_product(products, many=True)
        paginate_queryset = paginate.paginate_queryset(serialize, request)
        return paginate.get_paginated_response(paginate_queryset)
    
    def post(self, request):
        if not all(field in request.data for field in self.required_fields):
            return Response({"message": f"Please provide all required fields: {self.required_fields}"})
        
        user_id = get_user_token(request)
        
        Product.objects.create(
            title=self.request.data.get("title"),
            category_id=self.request.data.get("category"),
            details=self.request.data.get("details"),
            seller=user_id['pk']
        )
        return Response({"message": "the Product has been created successfully!"}, status=status.HTTP_200_OK)
    
    def put(self, request):
        if not "product-id" in request.headers:
            return Response({"message": "Please Provide Product ID You want to Edit!"}, status=status.HTTP_400_BAD_REQUEST)
        
        product_id = request.headers.get("product-id")
        user_id = get_user_token(request)

        product = Product.objects.select_related("category").filter(
            Q(pk=product_id) &
            Q(seller=user_id)
        )
        if not product.exists():
            return Response({"message": "this Product does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        title = request.data.get("title")
        category = request.data.get("category")
        details = request.data.get("details")

        product = product.first()
        product.title = title if title is not None else product.title
        product.category = category if category is not None else product.category
        product.details = details if details is not None else product.details
        product.save()
        
        return Response(
            {
                "message": "the Product has been edited successfully!"
            }, status=status.HTTP_200_OK
        )
    
    def delete(self, request):
        if not "product-id" in request.headers:
            return Response({"message": "Please Provide Product ID You want to Edit!"}, status=status.HTTP_400_BAD_REQUEST)
        
        product_id = request.headers.get("product-id")
        user_id = get_user_token(request)

        product = Product.objects.select_related("category").filter(
            Q(pk=product_id) &
            Q(seller=user_id)
        )
        if not product.exists():
            return Response({"message": "this Product does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        product.delete()
        return Response(
            {
                "message": "the Product has been deleted successfully!"
            }, status=status.HTTP_200_OK
        ) 


