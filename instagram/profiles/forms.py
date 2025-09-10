from django import forms
from myuser.models import MyUser

class LoginForm(forms.Form):
    phone = forms.CharField()
    password = forms.CharField(max_length=250,widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(max_length=250,widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=250,widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['username','phone','email','first_name','last_name',]

class ChangeProfile(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['image','bio','first_name','username']