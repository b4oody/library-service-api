from rest_framework import viewsets

from service.models import Author, Book
from service.serializers import (
    AuthorSerializer,
    BookSerializer,
)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
