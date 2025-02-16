from django.http import HttpResponse
from rest_framework import viewsets, generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from service import permissions
from service.models import Author, Book, Borrowing
from service.serializers import (
    AuthorSerializer,
    BookListSerializer,
    BookCreateSerializer,
    BorrowingListSerializer,
    BorrowingCreateSerializer,
    ReturnBookSerializer,
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


class ReturnBookBorrowing(
    generics.RetrieveAPIView,
    generics.UpdateAPIView
):
    queryset = Borrowing.objects.all()
    serializer_class = ReturnBookSerializer

    def put(self, *args, **kwargs):
        borrowing = self.get_object()
        if not borrowing.is_active:
            raise ValidationError({"borrowing": "This book have returned."})
        borrowing.is_active = False
        borrowing.book.inventory += 1
        borrowing.book.save()
        borrowing.save()
        return HttpResponse(
            "The book have returned success!",
            status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        self.put()
