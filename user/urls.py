from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import (
    UserCreateView,
    LoginUserView,
    ManageUserView,
)

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserCreateView.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]

app_name = "user"
