from django.urls import include, path
from rest_framework import routers

from service.views import (
    AuthorViewSet,
)

router = routers.DefaultRouter()
router.register(r"authors", AuthorViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "library-service"
