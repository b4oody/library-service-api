# Generated by Django 5.1.6 on 2025-02-16 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("service", "0004_remove_book_author_alter_book_title_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="borrowing",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
