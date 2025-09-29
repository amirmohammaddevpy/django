from django.urls import path
from . import views

urlpatterns = [
    path('',views.rooms,name="rooms"),
    path("chat/room/<int:pk>/",views.caht_rooms,name="chat_room"),
    path("room/update/<int:pk>/",views.update_room,name='update_room'),
    path("room/delete/<int:pk>/",views.delete_room,name='delete_room'),
    path("create/",views.create_room,name="create_room"),
    path("login/",views.loginpage,name="login_register"),
    path("logout/",views.logoutuser,name="logout"),
    path("register/",views.registerpage,name="register"),
    path("delete/message/<int:pk>/",views.deletemessage,name="delete_message"),
    path("profile/<int:pk>",views.profileuser,name="profile"),
    path("update/<int:pk>",views.updateimage,name="update_image"),
    path("join/group/<int:pk>",views.add_user,name="join"),
    path("leave/group/<int:pk>/",views.leave_user,name="leave"),
]