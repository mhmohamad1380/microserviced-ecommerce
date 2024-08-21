from django.urls import path
from .views import RegisterView, LoginView, user_validation, DecodeTokenView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("validate/", user_validation, name="validate"),
    path("decode-token/", DecodeTokenView.as_view(), name="decode-token"),
]