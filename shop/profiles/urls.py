from django.urls import path
from . import views

urlpatterns = [
    path("<str:uauthor>/",views.profile,name="profile"),
    path("edite/<str:uauthor>/",views.edite_profile,name="edite_profile_user"),
]
