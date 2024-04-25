from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path("", views.home, name="home"),
    # name=room is used inside the url jinja inside the html, so even if our actual url change, we can still access it using the name=room and does not need to change anything
    path("room/<str:pk>/", views.room, name="room"), # str represents string and pk is primary key, although we will be using int but we have written str here
    path("create-room/", views.createRoom, name='create-room'),
    path("update-room/<str:pk>", views.updateRoom, name='update-room'),
    path("delete-room/<str:pk>", views.deleteRoom, name='delete-room'),
    
]