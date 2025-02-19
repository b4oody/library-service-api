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
from telegram_bot.models import TelegramUser
from telegram_bot.utilities import send_telegram_message


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

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [permissions.IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(BorrowingSerializerViewSet, self).get_permissions()

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
        borrowing = serializer.save(user=self.request.user)

        try:
            telegram_user = TelegramUser.objects.get(user=self.request.user)
            telegram_id = telegram_user.telegram_id

            message = (
                f"*Вітаємо {telegram_user.user}!* \n\n"
                f"Ваше запозичення №{borrowing.id} було успішно створено.\n\n"
                f"*Запозичена книга*: {borrowing.book}\n"
                f"*Дата позичання*: {borrowing.borrow}\n"
                f"*Повернути до*: {borrowing.expected_return}\n\n"
                f"Бажаємо приємного читання!"
            )

            send_telegram_message(telegram_id, message)

        except TelegramUser.DoesNotExist:
            print(f"Не знайдено Telegram ID для користувача {self.request.user.username}")


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
        telegram_user = TelegramUser.objects.get(user=self.request.user)
        telegram_id = telegram_user.telegram_id
        message = (
            f"*Вітаємо {telegram_user.user}!* \n\n"
            f"Ваше запозичення №{borrowing.id} було успішно повернуто.\n\n"
            f"*Запозичена книга*: {borrowing.book}\n"
            f"*Дата позичання*: {borrowing.borrow}\n"
            f"*Повернуто*: {borrowing.actual}\n\n"
            f"Дякую за співпрацю!"
        )
        send_telegram_message(telegram_id, message)
        return HttpResponse(
            "The book have returned success!",
            status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        self.put()
