from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name="register"),
    path("login/",views.login_user,name="login"),
    path("logout/",views.logout_user,name="logout"),
    path("verify/",views.code_verify,name="verify"),
    path("resend/code",views.resend_code,name="resend_code")
]