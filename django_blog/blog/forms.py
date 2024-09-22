from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from .models import Comment
from taggit.forms import TagWidget

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Include 'tags' field
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),  # Optional widget for title
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),  # Optional widget for content
            'tags': TagWidget(attrs={'class': 'form-control'}),  # Use TagWidget for tag field
        }
    
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