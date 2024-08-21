from django.urls import path
from .views import GetUser

urlpatterns = [
    path("check/", GetUser.as_view(), name="check")
]