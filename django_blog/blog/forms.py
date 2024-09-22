from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from .models import Comment
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class PostForm(forms.ModelForm):
    class meta:
        model = Post
        fields = ['title','content']

class CommentForm(forms.ModelForm):
    class meta:
        model = Comment
        fields = ['content']
        widjets = {
            'content': forms.Textarea(attrs={'class': 'form-control','rows': 3}),

        }
        labels = {
            'content': 'Add your comment here:',
        }