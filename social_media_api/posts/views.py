from django.shortcuts import render
from rest_framework import viewsets, permissions, serializers
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import action


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

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