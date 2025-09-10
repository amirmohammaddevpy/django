from django.urls import path
from . import views

urlpatterns = [
    path("",views.view_cart,name="cart"),
    path("add/<int:id>/",views.add_cart,name="add"),
    path("remove/<int:id>/",views.cart_from_remove,name="remove"),
]
