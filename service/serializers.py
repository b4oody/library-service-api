from django.db import transaction
from rest_framework import serializers

from service.models import (
    Author,
    Book,
    Borrowing,
)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name"]


class AuthorListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField()

    class Meta:
        model = Author
        fields = ["id", "full_name"]


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "cover",
            "inventory",
            "daile_free"
        ]


class BookListSerializer(BookCreateSerializer):
    author = AuthorListSerializer(many=True, read_only=True)


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        if "request" in self.context:
            user = self.context["request"].user
            if not user.is_staff:
                self.fields.pop("user", None)


class BorrowingCreateSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Borrowing
        fields = [
            "id",
            "user",
            "borrow",
            "expected_return",
            "actual",
            "book",
            "is_active"
        ]
        extra_kwargs = {"is_active": {"read_only": True}}

    @transaction.atomic
    def create(self, validated_data):
        book = validated_data.get("book")
        if book.inventory <= 0:
            raise serializers.ValidationError("This book is out of stock")
        borrow = Borrowing.objects.create(**validated_data)
        book.inventory -= 1
        book.save()
        return borrow


class BorrowingListSerializer(BorrowingCreateSerializer):
    book = serializers.CharField(source="book.title")


class ReturnBookSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source="book.title", read_only=True)

    class Meta:
        model = Borrowing
        fields = ["id", "book", "is_active"]
