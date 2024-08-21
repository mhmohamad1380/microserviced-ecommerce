from rest_framework import status
from rest_framework.response import Response

def default_error(message: str):
    return Response(
        {
            "message": message
        }, status=status.HTTP_400_BAD_REQUEST
    )