# Generated by Django 5.1.6 on 2025-02-22 12:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
            ],
            options={
                "unique_together": {("first_name", "last_name")},
            },
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, unique=True)),
                (
                    "cover",
                    models.CharField(
                        choices=[("HARD", "Hard"), ("SOFT", "Soft")], max_length=10
                    ),
                ),
                ("inventory", models.PositiveIntegerField(default=0)),
                ("daile_free", models.DecimalField(decimal_places=2, max_digits=6)),
                (
                    "author",
                    models.ManyToManyField(related_name="books", to="service.author"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Borrowing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("borrow", models.DateField()),
                ("expected_return", models.DateField()),
                ("actual", models.DateField()),
                ("is_active", models.BooleanField(default=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="borrowings",
                        to="service.book",
                    ),
                ),
            ],
        ),
    ]
