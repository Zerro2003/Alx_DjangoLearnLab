from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import get_user_model
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False)
    # Following field corrected
    following = models.ManyToManyField('accounts.CustomUser', related_name='followed_by', symmetrical=False, blank=True)