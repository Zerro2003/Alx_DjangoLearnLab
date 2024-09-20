from django.test import TestCase
from django.test import ApiTestCase
from rest_framework.test import APIClient
from .models import Book
from .serializers import BookSerializer
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView
from rest_framework import status
from django.contrib.auth import get_user_model
class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        Book.objects.all().delete()

class TestBookCreateView(APITestCase):
    def test_create_book_with_valid_data(self):
        data = {'title': 'Test Book', 'author': 'John Doe', 'publication_year': 2023}
        response = self.client.post('/api/books/', data=data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 1)

        book = Book.objects.get()
        serialized_data = BookSerializer(book).data
        self.assertEqual(response.data, serialized_data)

    def test_create_book_with_invalid_data(self):
        data = {'title': ''}  # Missing required field
        response = self.client.post('/api/books/', data=data, format='json')

        self.assertEqual(response.status_code, 400)  # Bad request due to missing data

class TestBookListView(APITestCase):
    def setUp(self):
        super().setUp()
        Book.objects.create(title='Book 1', author='Author 1', publication_year=2022)
        Book.objects.create(title='Book 2', author='Author 2', publication_year=2023)

    def test_list_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_title(self):
        response = self.client.get('/api/books/?title=Book 1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book 1')

    def test_search_by_author(self):
        response = self.client.get('/api/books/?search=Author 1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'Author 1')

    def test_order_by_publication_year(self):
        response = self.client.get('/api/books/?ordering=publication_year')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['publication_year'], 2022)  # Ascending order

        response = self.client.get('/api/books/?ordering=-publication_year')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['publication_year'], 2023)  # Descending order

# Add similar test cases for BookUpdateView and BookDeleteView

# Test permissions
class TestBookUpdateView(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test_user', password='secret')
        self.book = Book.objects.create(title='Test Book', author='John Doe', publication_year=2023)

    def test_update_book_authenticated(self):
        self.client.force_authenticate(self.user)

        data = {'title': 'Updated Title'}
        response = self.client.login(f'/api/books/{self.book.pk}/', data=data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.get(pk=self.book.pk).title, 'Updated Title')

    def test_update_book_unauthenticated(self):
        data = {'title': 'Updated Title'}
        response = self.client.put(f'/api/books/{self.book.pk}/', data=data, format='json')

        self.assertEqual(response.status_code, 401)