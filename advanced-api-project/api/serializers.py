


import datetime
from rest_framework import serializers
from .models import Book, Author

class BookSerializer(serializers.ModelSerializer):
  """Serializer for the Book model, including validation for publication year."""

  class Meta:
    model = Book
    fields = '__all__'

  def validate_publication_year(self, value):
    """
    Custom validation to ensure publication year is not in the future.
    Raises a serializers.ValidationError if the year is greater than the current year.
    """
    if value > datetime.datetime.now().year:
      raise serializers.ValidationError("Publication year cannot be in the future.")
    return value

class AuthorSerializer(serializers.ModelSerializer):
  """Serializer for the Author model, including nested Book serialization."""
  books = BookSerializer(many=True, read_only=True)  # Nested BookSerializer

  class Meta:
    model = Author
    fields = ('name', 'books')

  def to_representation(self, instance):
    """
    Overrides the default to_representation method to include nested book data.
    """
    data = super().to_representation(instance)
    return data