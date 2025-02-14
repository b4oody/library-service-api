from django.contrib import admin

from service.models import Book, Borrowing

admin.site.register(Book)
admin.site.register(Borrowing)
