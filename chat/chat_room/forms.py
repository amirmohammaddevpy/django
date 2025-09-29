from django import forms
from .models import Room ,ProfileUser

class CreateRoom(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['topic','name','description','image']

class UpdateRoom(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['topic','name','description','image']

class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = ProfileUser
        fields = ['image',]