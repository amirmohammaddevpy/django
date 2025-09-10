from django import forms
from .models import Comment
from cart.models import CartItem

class CommentForms(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)

