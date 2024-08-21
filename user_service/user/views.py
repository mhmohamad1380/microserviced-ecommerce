from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .utils import default_error

class GetUser(APIView):
    def get(self, request):
        if not "uuid" in request.GET:
            return default_error(message="please provide a uuid!")
        uuid = request.GET.get("uuid")
        user = User.objects.filter(uuid=uuid)
        if not user.exists():
            return Response(
            {
                "exist": False,
            }, status=status.HTTP_200_OK
        )
        
        return Response(
            {
                "exist": True
            }, status=status.HTTP_200_OK
        )
    
