from django.urls import path
from . import views

app_name = "base"

urlpatterns = [
    path("", views.home, name="home"),
    path("room/<str:pk>/", views.room, name="room"),
    path("profile/<str:pk>/", views.userprofile, name="user-profile"),
    path("create-room/", views.createroom, name="createRoom"),
    path("update-room/<str:pk>/", views.updateroom, name="updateRoom"),
    path("delete-room/<str:pk>/", views.deleteroom, name="deleteRoom"),
    path("loginpage/", views.loginpage, name="loginpage"),
    path("logoutpage/", views.logoutpage, name="logoutpage"),
    path("resgister/", views.register, name="register"),
    path("delete-message/<str:pk>/", views.deletemessage, name="delete-message"),
]
