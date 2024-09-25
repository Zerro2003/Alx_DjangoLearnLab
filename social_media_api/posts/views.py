from django.shortcuts import render
from rest_framework import viewsets, permissions, serializers
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    @action(detail=False, methods=['get']) 

    def feed(self, request):
        user = request.user
        followed_users = user.following.all()
        feed_posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')
        serializer = self.get_serializer(feed_posts, many=True)
        return Response(serializer.data)
    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return permission_classes()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Set current user as author

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return permission_classes()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Set current user as author

        # Additional check to ensure user can only comment on existing posts
        post_id = self.request.data.get('post')
        if not Post.objects.filter(pk=post_id).exists():
            raise serializers.ValidationError('Invalid post ID provided')
        
class FollowingPostsListView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        # Assuming following_users is accessible from the request or view context
        following_users = self.request.user.following.all()  # Replace with your logic
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')  # Order by descending creation date
        return posts