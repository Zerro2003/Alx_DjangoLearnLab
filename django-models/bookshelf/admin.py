from django.contrib import admin
from .models import Book
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Display these fields in the list view
    list_filter = ('author', 'publication_year')  # Add filters for these fields
    search_fields = ('title', 'author')  # Enable search for these fields
admin.site.register(Book,BookAdmin)
