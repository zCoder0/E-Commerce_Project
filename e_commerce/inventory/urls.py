from django.contrib import admin
from django.urls import path
from inventory import views
from django.conf import settings
from django.conf.urls.static import static

inventory_urlpatterns = [
    path("admin_login/",views.admin_login ,name='admin_login'),
    path("inventory_management/", views.inventory_management, name="inventory_management"),
    path("add_product/", views.add_product_request, name="add_product_request"),
    path("update_products/<int:product_id>/", views.update_product_request, name="update_product_request"),
    path("delete_product_request/<int:product_id>/", views.delete_product_request, name="delete_product_request"),

#category
    path("categories/", views.category_management, name="category_management"),
    path("add_category/", views.add_category_request, name="add_category_request"),
    path("update_category/<int:category_id>/", views.update_category_request, name="update_category_request"),
    path("delete_category/<int:category_id>/", views.delete_category_request, name="delete_category_request"),
    
#products
    path("product_details/<int:product_id>", views.product_details, name="product_details"),

#suppliers
    path('suppliers_management/',views.suppliers_management ,name="suppliers_management"),
    path('add_supplier/',views.add_supplier ,name='add_supplier'),
    path("update_supplier/<int:supplier_id>/", views.update_supplier_request, name="update_supplier_request"),
    path("delete_supplier_request/<int:supplier_id>/", views.delete_supplier_request, name="delete_supplier_request"),

#stock
    path("inventory_dashboard/",views.inventory_dashboard ,name='inventory_dashboard'),
    path("export_stock_csv/" ,views.export_stock_csv ,name="export_stock_csv"),
] 
