from rest_framework import viewsets

from service import permissions
from service.models import Author, Book, Borrowing
from service.serializers import (
    AuthorSerializer,
    BookListSerializer,
    BookCreateSerializer,
    BorrowingSerializer,
)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    # permission_classes = [permissions.IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BookListSerializer
        return BookCreateSerializer


class BorrowingSerializerViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
