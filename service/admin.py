from django.contrib import admin

from service.models import Book, Borrowing, Author

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Borrowing)
