from django import forms
from .models import Profiles


class ProfileForms(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = ("image","phone","address")
    
