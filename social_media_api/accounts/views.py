from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Responsefrom
from rest_framework.generics import GenericAPIView
from rest_framework import generics.GenericAPIView
from rest_framework.permissions import permissions.IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({"user": serializer.data, "token": token.key})
class FollowViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def follow_user(self, request, pk):
        user_to_follow = CustomUser.objects.get(pk=pk)
        if user_to_follow != request.user:
            request.user.following.add(user_to_follow)
            return Response({'message': 'Following successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

    def unfollow_user(self, request, pk):
        user_to_unfollow = CustomUser.objects.get(pk=pk)
        request.user.following.remove(user_to_unfollow)
        return Response({'message': 'Unfollowed successfully'}, status=status.HTTP_200_OK)
        