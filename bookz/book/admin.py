from django.contrib import admin
from book.models import Book, Author, Publisher, Subject

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Subject)
