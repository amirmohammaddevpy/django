from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("detail/<int:id>/<slug:slug>",views.detail_post,name="detail"),
    path("create/",views.create_post,name="create"),
    path("post/like/",views.like_post,name="like"),
]
