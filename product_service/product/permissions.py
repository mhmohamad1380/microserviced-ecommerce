from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
import requests
from django.conf import settings

class IsAuthenticatedCustom(BasePermission):
    def has_permission(self, request, view):
        if not "Authorization" in request.headers:
            raise PermissionDenied("You are not Logged in!")
        token = request.headers.get('Authorization').split(' ')[1]
        response = requests.post(f"{settings.USER_SERVICE_ADDRESS}/user/auth/validate/", data={'token': token})
        return response.status_code == 200 and response.json().get('active', False)