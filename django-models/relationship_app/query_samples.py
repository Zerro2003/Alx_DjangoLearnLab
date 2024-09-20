# query_samples.py
import os
import django

# Set the settings module for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

# Initialize Django
django.setup()
# Import the necessary models
from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author (assuming the author's name is known)
author_name = "J.K. Rowling"
author = Author.objects.get(name=author_name)  # Find the author by name
books_by_author = Book.objects.filter(author=author)  # Get all books by this author

print(f"Books by {author_name}:")
for book in books_by_author:
    print(book.title)

# List all books in a specific library (assuming the library's name is known)
library_name = "Central Library"
library = Library.objects.get(name=library_name)  # Find the library by name
books_in_library = library.books.all()  # Get all books in this library

print(f"\nBooks in {library_name}:")
for book in books_in_library:
    print(book.title)

# Retrieve the librarian for a specific library
librarian = Librarian.objects.get(library=library)  # Find the librarian for the library

print(f"\nLibrarian for {library_name}: {librarian.name}")
