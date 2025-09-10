from django.contrib import admin
from .models import MyUser
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
# Register your models here.

class CaretionUserFroms(forms.ModelForm):
    password1 = forms.CharField(label="passwor",widget=forms.PasswordInput)
    password2 = forms.CharField(label="password confirm" ,widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ("phone","username","email","first_name","last_name",)

    def clean_passwords(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("password dos't macth")
        return password2
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ("phone","username","email","first_name","last_name","is_active","is_admin","is_staff")

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = CaretionUserFroms

    list_display = ("username","phone","email","first_name","last_name","is_admin","is_active","is_staff")
    list_filter = ("phone","username")
    fieldsets = (
        (None,{'fields':("email","username","password")}),
        ('personal info',{"fields":("first_name","last_name","phone","date_of_birth","bio",)}),
        ('Permission',{"fields":("is_staff","is_admin","is_active")}),
    )

    search_fields = ['username',]
    filter_horizontal = ()

admin.site.register(MyUser,UserAdmin)
admin.site.unregister(Group)