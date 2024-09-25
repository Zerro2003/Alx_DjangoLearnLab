from django.shortcuts import render
from rest_framework import viewsets, permissions, serializers
from .models import Post, Comment, Like
from rest_framework import status
from notifications.models import Notification
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes
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
        serializer.save(author=self.request.user)

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
        serializer.save(author=self.request.user)

        # Additional check to ensure user can only comment on existing posts
        post_id = self.request.data.get('post')
        if not Post.objects.filter(pk=post_id).exists():
            raise serializers.ValidationError('Invalid post ID provided')

class FollowingPostsListView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        following_users = self.request.user.following.all()
        posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')
        return posts

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    user = request.user

    # Check if user already liked the post
    like, created = Like.objects.get_or_create(user=user, post=post)
    if not created:
        return Response({'error': 'You already liked this post'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a notification for the post author (if not the current user)
    if user != post.author:
        Notification.objects.create(
            recipient=post.author,
            actor=user,
            verb='liked your post',
            target_content_type=ContentType.objects.get_for_model(Post),
            target_object_id=post.id
        )

    return Response({'message': 'Post liked successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    user = request.user

    try:
        like = Like.objects.get(user=user, post=post)
        like.delete()
    except Like.DoesNotExist:
        return Response({'error': 'You haven\'t liked this post yet'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Post unliked successfully'}, status=status.HTTP_200_OK)