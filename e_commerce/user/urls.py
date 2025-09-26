from django.contrib import admin
from django.urls import path
from user import views

user_urlpatterns = [
    path("",views.index ,name=""),
    path("user_signup.html",views.user_signup,name="user_signup"),
    path("user_signin.html",views.user_signin ,name="user_signin"),
    path("index.html",views.index ,name='index'),
    path("profile.html",views.profile ,name="profile"),
    path("mycart.html",views.myCart ,name="myCart"),
    path("logout",views.logout,name="logout"),
]