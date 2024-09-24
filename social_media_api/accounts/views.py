from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from .models import CustomUser
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