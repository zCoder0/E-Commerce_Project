from django.contrib import admin
from django.urls import path
from inventory import views
from django.conf import settings
from django.conf.urls.static import static

inventory_urlpatterns = [
    path("inventory/", views.inventory_home, name="inventory_home"),
    path("inventory_management/", views.inventory_management, name="inventory_management"),
    path("add_product/", views.add_product_request, name="add_product_request"),
    path("update_product/<int:product_id>/", views.update_product_request, name="update_product_request"),
    path("delete_product/<int:product_id>/", views.delete_product_request, name="delete_product_request"),

#category
    path("categories/", views.category_management, name="category_management"),
    path("add_category/", views.add_category_request, name="add_category_request"),
    path("update_category/<int:category_id>/", views.update_category_request, name="update_category_request"),
    path("delete_category/<int:category_id>/", views.delete_category_request, name="delete_category_request"),
    
#products
    path("product_details/<int:product_id>", views.product_details, name="product_details"),
] 
