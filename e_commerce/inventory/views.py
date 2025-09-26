from django.shortcuts import render,redirect
from inventory_action import *
# Create your views here.

def inventory_dashboard(request):
    pass 

def inventory_home(request):
    return render(request, "inventory/inventory_home.html")

def add_product(request):
    if request.method == "POST":
        flag = add_product(request)

        if flag:
            return redirect('inventory_home')
        else:
            return render(request, "inventory/add_product.html", {"error": 1})
    else:
        return render(request, "inventory/add_product.html")
    
def view_products(request):
    pass

def update_product(request, product_id):
    pass

def delete_product(request, product_id):
    pass
