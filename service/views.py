from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from service import permissions
from service.models import Author, Book, Borrowing
from service.serializers import (
    AuthorSerializer,
    BookListSerializer,
    BookCreateSerializer,
    BorrowingListSerializer,
    BorrowingCreateSerializer,
)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BookListSerializer
        return BookCreateSerializer


class BorrowingSerializerViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if user.is_staff:
            return queryset
        return queryset.filter(user=user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BorrowingListSerializer
        return BorrowingCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
