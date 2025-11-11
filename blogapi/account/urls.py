from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("profile/",views.ProfileUser.as_view(),name="profile"),
    path("register/",views.RegisterView.as_view(),name="register"),
    path("logout/",views.LogoutView.as_view(),name="logout"),
    path("login/",views.LoginView.as_view(),name="login"),
    path("refesh/token/",TokenRefreshView.as_view(),name="refresh_token"),
    path("token/",TokenObtainPairView.as_view(),name="token"),
]