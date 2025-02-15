from django.urls import include, path
from rest_framework import routers

from service.views import (
    AuthorViewSet,
    BookViewSet,
    BorrowingSerializerViewSet,
)

router = routers.DefaultRouter()
router.register(r"authors", AuthorViewSet)
router.register(r"books", BookViewSet)
router.register(r"borrowings", BorrowingSerializerViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "library-service"
