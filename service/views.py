from rest_framework import viewsets

from service.models import Author, Book, Borrowing
from service.serializers import (
    AuthorSerializer,
    BookSerializer,
    BorrowingSerializer,
)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BorrowingSerializerViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
