from django.db import models

from config.settings.base import AUTH_USER_MODEL


class Book(models.Model):
    class CoverType(models.TextChoices):
        hard = "HARD"
        soft = "SOFT"

    title = models.CharField(max_length=100)
    author = models.ManyToManyField(
        AUTH_USER_MODEL,
        related_name="books",
    )
    cover = models.CharField(
        max_length=10,
        choices=CoverType.choices
    )
    inventory = models.PositiveIntegerField(default=0)
    daile_free = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.title}({self.author})"


class Borrowing(models.Model):
    borrow = models.DateField()
    expected_return = models.DateField()
    actual = models.DateField()
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrowings",
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings",
    )

    def __str__(self):
        return f"{self.user}({self.borrow} - {self.expected_return})"
