from rest_framework import pagination
from rest_framework.response import Response


class CartPagination(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = "page"
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return Response(
            {
                "products": data
            }
        )