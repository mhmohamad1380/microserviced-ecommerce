from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import AccessToken
import jwt
from django.conf import settings

User = get_user_model()

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            "user": serializer.data,
            "uuid": user.pk,
            "access_token": access_token,
            "refresh_token": refresh_token
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                "access_token": access_token,
                "refresh_token": refresh_token
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        

@api_view(['POST'])
def user_validation(request):
    token = request.data.get("token")
    try:
        AccessToken(token)
        return Response({"active": True}, status=status.HTTP_200_OK)
    except:
        return Response({"active": False}, status=status.HTTP_400_BAD_REQUEST)
    

class DecodeTokenView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Decode the JWT token to get the payload
            token = AccessToken(token)
            user_id = token.payload['user_id']
            
            if not user_id:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

            # Optionally, fetch user details based on the user_id
            try:
                user = User.objects.get(pk=user_id)
                return Response({"user_id": user.pk}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError):
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

