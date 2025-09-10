from django.urls import path
from . import views

urlpatterns = [
    path("",views.list_products,name="list_product"),
    path("product/<str:slug>/",views.detail_product,name="detail_product"),
]
