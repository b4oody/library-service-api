from django.urls import include, path
from rest_framework import routers

from service.views import (
    AuthorViewSet,
    BookViewSet,
    BorrowingSerializerViewSet,
    ReturnBookBorrowing,
)

router = routers.DefaultRouter()
router.register(r"authors", AuthorViewSet)
router.register(r"books", BookViewSet)
router.register(r"borrowings", BorrowingSerializerViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "borrowings/<int:pk>/return/",
        ReturnBookBorrowing.as_view(),
        name="return_book_borrowing"
    ),
]

app_name = "library-service"
