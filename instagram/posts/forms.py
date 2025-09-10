from django import forms
from .models import Post ,CommentPost

class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image','caption']

class CommentPostForm(forms.ModelForm):
    class Meta:
        model = CommentPost
        fields = ['text',]