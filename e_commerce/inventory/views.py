from django.shortcuts import render,redirect
import csv
from django.http import HttpResponse
from inventory.models import *
from inventory.inventory_action import *
# Create your views here.
from user.views import PageNotFound

# Inventory Dashboard

def inventory_dashboard(request):
    try:
        category_details= get_all_categories()
        print(category_details)
        threshold = None
        stocks = []

        if request.method == "POST":
            category_id = request.POST["categoryID"]
            threshold = request.POST.get("threshold")
            print(category_id ,threshold)
            # Category filter
            if int(category_id):
                stocks = get_stock_by_category(category_id=category_id)
                print("Stocks ",stocks)
            else:
                stocks = get_all_stock()

            # Threshold filter (if provided)
            if threshold:
                try:
                    threshold = int(threshold)
                    stocks = [s for s in stocks if s["total_stock"] <= threshold]
                except ValueError:
                    pass
        else:
            stocks = get_all_stock()
        
        sum_stocks = sum(stock['total_stock']*stock['total_products'] for stock in stocks)
        total_products = sum(stock['total_products'] for stock in stocks)

        summary={
            "total_stocks":sum_stocks,
            "total_products":total_products
        }
        return render(
            request,
            "inventory/inventory_dashboard.html",
            {
                "stocks": stocks,
                "categories": category_details,
                "threshold": threshold,
                "summary":summary
                
            },
        )
    except Exception as e:
        print("Error in inventroy dashbiard ",e)
        return redirect('someThingWrong')

def admin_login(request):
    if request.method=="POST":
        user_name = request.POST['user_name']
        password = request.POST['password']

        if user_name.lower() == "admin" and password.lower()=="admin":
            return redirect('inventory_dashboard')
        else:
            return render(request,"inventory/admin_login.html",{'error':1})

    else:
        return render(request,"inventory/admin_login.html")



# category 

def category_management(request):
    try:
        if request.method == "GET":
            
            category_details = get_all_categories()
            if category_details:
                return render (request, "inventory/category_management.html" ,{'categories':category_details})
            else:
                return render(request, "inventory/category_management.html" ,{'error':1})
            
    except Exception as e:
        print("Error : ",e)
        return redirect('inventory_dashboard')
    
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
        category_details = get_category_by_id(category_id)

        if category_details:
            return render(request, "inventory/update_category.html", {'category': category_details})
        else:
            return redirect('PageNotFound')

def delete_category_request(request, category_id):

    flag = delete_category(category_id)

    if flag:
        return redirect('category_management')
    else:
        return render(request, "inventory/category_management.html", {"error": 1})




#Product Details

def inventory_management(request):
    try:
        if request.method == "GET":
            products_details = get_all_products()
            return render(request, "inventory/inventory_management.html" ,{'products':products_details})
    except Exception as e:
        return redirect("someThingWrong")
    
def product_details(request, product_id):
    try:
        if request.method == "GET":
            product_details = get_product_by_id(product_id)
            return render(request, "inventory/product_details.html", {'product': product_details})

    except Exception as e:
        print(f"Error in product details view: {e}")
        return render(request, "inventory/product_details.html", {"error": 1})

def add_product_request(request):
    try:
        if request.method == "POST":
            flag = add_product(request)

            if flag:
                return redirect('inventory_management')
            else:
                return render(request, "inventory/add_product.html", {"error": 1})
        else:
            category_details = get_all_categories()
            suppliers_details = get_all_suppliers()
            return render(request, "inventory/add_product.html",{"suppliers":suppliers_details,"categories":category_details})
        
    except Exception as e:
        print("Error is add product request : ",e)
        return redirect('PageNotFound')
    
def update_product_request(request, product_id):
    try:
        
        if request.method == "POST":
            flag = update_product(request, product_id)

            if flag:
                return redirect('inventory_management')
            else:
                return render(request, "inventory/update_products.html", {"error": 1})
        else:
            product_details = get_product_by_id(product_id)
            return render(request, "inventory/update_products.html", {'product': product_details})
        
    except Exception as e:
        print("Error in update product request ",e)
        return redirect("someThingWrong")
    
def delete_product_request(request, product_id):
    
    try:
        flag = delete_product(product_id)

        if flag:
            return redirect('inventory_management')
        else:
            return render(request, "inventory/inventory_management.html", {"error": 1})

    except Exception as e:
        return redirect("someThingWrong")



#Manage Orders

def manage_orders(request):
    try:
        orders = get_all_orders()

        if request.method == "POST":
            action = request.POST.get("action")

            if action == "filter_area":
                orders = get_order_by_area(request)

            elif action == "update_status":
                flag = update_order_status(request)
                if flag:
                    return redirect('manage_orders')
                else:
                    return render(request, 'inventory/manage_orders.html', {
                        'orders': orders,
                        'error': 1
                    })

        return render(request, 'inventory/manage_orders.html', {
            'orders': orders
        })

    except Exception as e:
        print("Error in manage_orders:", e)
        return redirect('someThingWrong')


#Supplier

def suppliers_management(request):
    try:
    
        supplier_details = get_all_suppliers()
        
        return render(request ,'inventory/suppliers_management.html',{'suppliers':supplier_details})
    except Exception as e:
        print("Error in supplier management : ",e)
        return redirect("someThingWrong")
    
def add_supplier(request):
    try:
        if request.method=="POST":
            flag = add_supplier_details(request)
            if flag:
                return redirect('suppliers_management')
            else:
                return render(
                    request,
                    'inventory/add_supplier.html',
                    {
                        'error':1
                    }
                )
        return render(request , 'inventory/add_supplier.html')
    except Exception as e:
        print("Error in add supplier ",e)
        return redirect("someThingWrong")

def update_supplier_request(request , supplier_id):
    try:
        if request.method == "POST":
            flag = update_supplier(request, supplier_id)

            if flag:
                return redirect('suppliers_management')
            else:
                return render(request, "inventory/update_supplier.html", {"error": 1})
        else:

            supplier_details= get_supplier_by_id(supplier_id)
            
            return render(request, "inventory/update_supplier.html", {'supplier': supplier_details})
    except Exception as e:
        return redirect("someThingWrong")

def delete_supplier_request(request,supplier_id):
    try:
        flag = delete_supplier(supplier_id)
        if flag:
            return redirect('suppliers_management')
        else:
            return render(request, "inventory/suppliers_management.html", {"error": 1})
    except Exception as e:
        return redirect("someThingWrong")


#stock

def export_stock_csv(request):
    try:
        # Get all stocks (or you can reuse filters from POST/GET if needed)
        stocks = get_all_stock()  # Or apply category/threshold filter if passed as GET params

        # Create the HttpResponse object with CSV header
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="stock_data.csv"'

        writer = csv.writer(response)
        # Write CSV header
        writer.writerow(['Product', 'Category', 'Supplier', 'Address', 'Stock', 'Total Products'])

        # Write stock rows
        for stock in stocks:
            writer.writerow([
                stock['product_name'],
                stock['category_name'],
                stock['supplier_name'],
                stock['address'],
                stock['total_stock'],
                stock['total_products']
            ])

        return response

    except Exception as e:
        return redirect("someThingWrong")
