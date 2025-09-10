from . import views
from django.urls import path

urlpatterns = [
    path("<str:user>/",views.checkout,name="checkout")
]
