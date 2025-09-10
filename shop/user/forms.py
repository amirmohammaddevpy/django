from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Register(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ("username","first_name","last_name","email","password",)
    
    def clean(self):
        clean_data = super().clean()
        if clean_data.get('password') != clean_data.get("password_confirmation"):
            raise ValidationError("Passwords do not match.")
        else:
            return clean_data
        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=250,label="Username")
    password = forms.CharField(widget=forms.PasswordInput,label="Password")

class CodeRegister(forms.Form):
    code = forms.CharField(max_length=5)
