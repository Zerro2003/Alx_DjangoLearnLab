from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('', views.home, name='home'),
    path('comment/new/<int:post_id>/', views.CommentCreateView, name='comment-create'),
    path('post/', PostListView.as_view(), name='posts'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('comment/<int:pk>/update/', views.CommentUpdateView, name='edit_comment'),
    path('comments/<int:pk/comments/new', views.CommentCreateView, name='post-comments-create'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView, name='delete_comment'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comments/new/', views.CommentCreateView, name='post-comments-create'),
]  
