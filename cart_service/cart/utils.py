import requests
from django.conf import settings
from rest_framework.response import Response

def get_user_token(request):
    token = request.headers.get('Authorization').split(' ')[1]
    request = requests.post(f"{settings.USER_SERVICE_ADDRESS}/user/auth/decode-token/", data={"token": token})
    if request.status_code == 200:
        return {"pk": request.json().get("user_id")}
    return Response({"error": request.json().get("error")})