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
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({'error': 
 'Post not found'}, status=status.HTTP_404_NOT_FOUND) 


    user = request.user

    # Check if user already liked the post
    if Like.objects.filter(user=user, post=post).exists():
        return Response({'error': 'You already liked this post'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new Like object
    like = Like.objects.create(user=user, post=post)

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
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({'error': 
 'Post not found'}, status=status.HTTP_404_NOT_FOUND)  


    user = request.user

    # Check if user has liked the post
    like = Like.objects.filter(user=user, post=post)
    if not like.exists():
        return Response({'error': 'You haven\'t liked this post yet'}, status=status.HTTP_400_BAD_REQUEST)

    # Delete the Like object
    like.delete()

    return Response({'message': 'Post unliked successfully'}, status=status.HTTP_200_OK)