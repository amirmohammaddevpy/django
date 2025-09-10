from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path("",views.home_page,name="home_page"),
    path("explor/",views.explor,name="explor"),
]
