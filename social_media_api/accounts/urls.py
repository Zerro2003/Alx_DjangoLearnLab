from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('follow/<int:pk>/', views.FollowViewSet.as_view({'post': 'follow_user'}), name='follow-user'),
    path('unfollow/<int:pk>/', views.FollowViewSet.as_view({'post': 'unfollow_user'}), name='unfollow-user'),
]