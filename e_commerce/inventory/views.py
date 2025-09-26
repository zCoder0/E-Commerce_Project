from django.shortcuts import render,redirect
from inventory.inventory_action import *
# Create your views here.


# Inventory Dashboard

def inventory_dashboard(request):
    pass 

def inventory_home(request):
    return render(request, "inventory/inventory_home.html")

def inventory_management(request):
    if request.method == "GET":
        produts = get_all_products()

        products_details = [
            {
                "product_id": product[0],
                "product_name": product[1],
                "description": product[2],
                "price": product[3],
                "stock": product[5],
                "category_id": product[6],
                "supplier_id": product[7],
                "image_url": product[11],
            }
            for product in produts
        ]

        return render(request, "inventory/inventory_management.html" ,{'products':products_details})

def add_product_request(request):
    if request.method == "POST":
        flag = add_product(request)

        if flag:
            return redirect('inventory_management')
        else:
            return render(request, "inventory/add_product.html", {"error": 1})
    else:
        categories = get_all_categories()
        suppliers = get_all_suppliers()

        category_details =[
            {
                "category_id": category[0],
                "category_name": category[1],
            }
            for category in categories
        ]

        suppliers_details =[
            {
                "supplier_id": supplier[0],
                "supplier_name": supplier[1],
            }
            for supplier in suppliers
        ]
        return render(request, "inventory/add_product.html",{"suppliers":suppliers_details,"categories":category_details})
    
def update_product_request(request, product_id):
    if request.method == "POST":
        flag = update_product(request, product_id)

        if flag:
            return redirect('inventory_management')
        else:
            return render(request, "inventory/update_products.html", {"error": 1})
    else:
        product = get_product_by_id(product_id)
        product_details = {
                "product_id": product[0],
                "product_name": product[1],
                "description": product[2],
                "price": product[3],
                "offer": product[4],
                "disscount_price": product[3] - (product[3]*product[4]/100),
                "stock": product[5],
                "category_id": product[6],
                "supplier_id": product[7],
                "image_url": product[12],
            }
        
        return render(request, "inventory/update_products.html", {'product': product_details})

def delete_product_request(request, product_id):
    flag = delete_product(product_id)

    if flag:
        return redirect('inventory_management')
    else:
        return render(request, "inventory/inventory_management.html", {"error": 1})
    

#category 

def category_management(request):
    if request.method == "GET":
        categories = get_all_categories()

        category_details = [
            {
                "category_id": category[0],
                "category_name": category[1],
                "description": category[2],
            }
        for category in categories]

        return render (request, "inventory/category_management.html" ,{'categories':category_details})
    
def add_category_request(request):
    if request.method == "POST":
        flag = add_category(request)

        if flag:
            return redirect('category_management')
        else:
            return render(request, "inventory/add_category.html", {"error": 1})
    else:
        return render(request, "inventory/add_category.html")
    
def update_category_request(request, category_id):
    if request.method == "POST":
        flag = update_category(request, category_id)

        if flag:
            return redirect('category_management')
        else:
            return render(request, "inventory/update_category.html", {"error": 1})
    else:
        category = get_category_by_id(category_id)
        category_details = {
            "category_id": category[0],
            "category_name": category[1],
            "description": category[2],
        }
        return render(request, "inventory/update_category.html", {'category': category_details})

def delete_category_request(request, category_id):
    flag = delete_category(category_id)

    if flag:
        return redirect('category_management')
    else:
        return render(request, "inventory/category_management.html", {"error": 1})

#Supplier

def supplier_management(request):

    pass

#Product Details

def product_details(request, product_id):
    try:
        if request.method == "GET":
            product = get_product_by_id(product_id)
            product_details = {
                "product_id": product[0],
                "product_name": product[1],
                "description": product[2],
                "price": product[3],
                "offer": product[4],
                "stock": product[5],
                "image_url": product[11],
                "category_name": product[13],
                "supplier_name": product[14],
                "disscount_price": product[3] - (product[3]*product[4]/100),
            }
            return render(request, "inventory/product_details.html", {'product': product_details})

    except Exception as e:
        print(f"Error in product details view: {e}")
        return render(request, "inventory/product_details.html", {"error": 1})
    