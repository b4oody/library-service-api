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

    def validate_inventory(self, inventory):
        if inventory <= 0:
            raise serializers.ValidationError("Inventory must be greater than 0")


class BookListSerializer(BookCreateSerializer):
    author = AuthorListSerializer(many=True, read_only=True)


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source="book.title")
    user = serializers.CharField(source="user.username")

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow",
            "expected_return",
            "actual",
            "book",
            "user"
        ]
