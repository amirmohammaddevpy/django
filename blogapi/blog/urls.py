from django.urls import path
from . import views

urlpatterns = [
    path("",views.ListView.as_view(),name="listview"),
    path("<int:pk>/",views.DetailView.as_view(),name="detail"),
    path("create-API",views.CreateAPI.as_view(),name="create"),
]