from django.contrib import admin
from django.urls import path
from inventory import views

inventory_urlpatterns = [
    path("inventory/", views.inventory_home, name="inventory_home"),
    path("add_product/", views.add_product, name="add_product"),
    path("view_products/", views.view_products, name="view_products"),
    path("update_product/<int:product_id>/", views.update_product, name="update_product"),
    path("delete_product/<int:product_id>/", views.delete_product, name="delete_product"),

    
]
