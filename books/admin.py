from django.contrib import admin
from .models import Book, Author, Rate

class BookAdmin(admin.ModelAdmin):
    pass
admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Rate)