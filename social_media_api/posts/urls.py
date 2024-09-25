from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.contrib import admin
router = DefaultRouter()
router.register('posts', views.PostViewSet)
router.register('comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/', include('posts.urls')),
    path('feed/', views.PostViewSet.as_view({'get': 'feed'}), name='feed'),
    path('posts/<int:pk>/like/', views.like_post, name='like-post'),
    path('posts/<int:pk>/unlike/', views.unlike_post, name='unlike-post'),
]