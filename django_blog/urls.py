from django.urls import path, include

urlpatterns = [
    path('', include('blog.urls')),  # Make sure to add this to include your blog URLs
]
