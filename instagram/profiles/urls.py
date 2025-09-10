from django.urls import path
from . import views

app_name = "profile"

urlpatterns = [
    path("register/",views.register_form,name="register"),
    path("login/",views.login_user,name="login"),
    path("verify/",views.verify_code,name="verify"),
    path("resend/",views.resend_code,name="resend"),
    path("change/profile/<str:user>",views.change_form,name="change_form"),
    path("follow/",views.user_fllowing,name="follow"),
    path("profile/<str:username>/",views.dashbord,name="profile"),
]