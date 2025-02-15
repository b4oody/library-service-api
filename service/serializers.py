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
    class Meta:
        model = Author
        fields = ["id", "full_name"]


class BookSerializer(serializers.ModelSerializer):
    author = AuthorListSerializer(many=True)

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
