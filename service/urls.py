from django.urls import include, path
from rest_framework import routers

from service.views import (
    AuthorViewSet,
    BookViewSet,
)

router = routers.DefaultRouter()
router.register(r"authors", AuthorViewSet)
router.register(r"books", BookViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "library-service"
