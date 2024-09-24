from rest_framework import serializers
from django.contrib.auth.models import get_user_model
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
  # Use get_user_model for custom user
        fields = ('id', 'username', 'email', 'password', 'bio', 'profile_picture', 'followers')
        write_only_fields = ('password',)
        username = serializers.CharField()

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        token, created = Token.objects.create(user=user)
        return user, token