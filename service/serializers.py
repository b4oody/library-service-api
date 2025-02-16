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


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow",
            "expected_return",
            "actual",
            "book",
        ]

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
