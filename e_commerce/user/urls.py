from django.contrib import admin
from django.urls import path
from user import views

user_urlpatterns = [
    path("",views.index ,name=""),
    path("user_signup.html",views.user_signup,name="user_signup"),
    path("user_signin.html",views.user_signin ,name="user_signin"),
    path("index.html",views.index ,name='index'),
    path('chatBot/',views.chatBot,name="chatBot"),
    path("profile.html",views.profile ,name="profile"),
    path("add_new_address/<int:user_id>" , views.add_new_address , name ="add_new_address "),
    path("product_details/<int:product_id>/", views.view_product_details, name="view_product_details"),
    path("add_cart/<int:product_id>/", views.add_cart, name="add_cart"),
    path("mycart.html",views.myCart ,name="myCart"),
    path("remove_cart/<int:cart_id>/",views.remove_cart_item ,name="remove_cart_item"),
    path("update_cart/<int:cart_id>/",views.update_cart_item ,name="update_cart_item"),
    path("buy_product/",views.buy_product ,name="buy_product"),
    path("myorders/",views.myorders,name="myorders"),
    path('cancel_myorder/<int:order_id>',views.cancel_myorder,name='cancel_myorder'),
    path("logout",views.logout,name="logout"),
]