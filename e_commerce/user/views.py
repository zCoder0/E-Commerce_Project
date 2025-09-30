from django.shortcuts import render,redirect
from user.user_action import *
from e_commerce.chatbot import *
from user.models import *   


user_id = None


cb = ChatBot()
cb.train_model()

def PageNotFound(request):
    return render(request , 'pagenotfound.html')

def index_main(request):
    return render(request ,"index_main.html" )

def index(request):
    user_id =  request.session.get("user_id",0)

    if not user_id:
        return redirect("user_signin")
    
    products = get_all_products()
    return render(request , "user/index.html" ,{"products":products})

def user_signup(request):

    if request.method == "POST":
        user_name = request.POST['user_name']
        user_email = request.POST['user_email']
        user_password = request.POST['user_password']
        user_mobile = request.POST['user_mobile']

        user = UserRegister.objects.create(
                            user_name= user_name , 
                             user_mobile=user_mobile,
                             user_email=user_email,
                             user_password=user_password)
        user.save()
        
        if user.id:
            return redirect("user_signin")
        else:
            return render(request ,"user/user_signup.html",{"error":1})
        
    else:
        return render(request , "user/user_signup.html")

def user_signin(request):
    if request.method == "POST":
        user_email = request.POST['user_email']
        user_password = request.POST['user_password']

        data = UserRegister.objects.get(user_email = user_email ,
                                        user_password = user_password)
        
        if data :
            request.session["user_id"] = data.id
            return redirect("index")
        
        else:
            return render(request ,"user/user_signin.html",{"error":1})
        
    else:
        return render(request , "user/user_signin.html")
    
def profile(request):
    user_id = request.session.get("user_id", 0)

    if not user_id:
        return redirect("user_signin")

    try:
        if request.method == "GET":
            datas = get_full_details(uid=user_id)

            if datas:
                return render(request, "user/profile.html", {"user_data": datas})
            else:
                return render(request, "user/profile.html", {"error": 404})

        elif request.method == "POST":
            user_id = request.POST['user_id']
            user_address = request.POST['address']
            user_city = request.POST['city']
            user_state = request.POST['state']
            user_zipcode = request.POST['zipcode']
            user_country = request.POST['country']

            flag = update_user_details(
                user_id=user_id,
                address=user_address,
                city=user_city,
                state=user_state,
                zipcode=user_zipcode,
                country=user_country
            )

            if flag:
                return redirect("profile")
            else:
                return render(request, "user/profile.html", {"error": 404})

    except Exception as e:
        print("Error ", e)
        return redirect("index")

def add_new_address(request,user_id):
    try:
        if request.method == "POST":
            pass

    except Exception as e:
        print("Error in add new address : ",e)
        return False


#view prdocts

def view_product_details(request,product_id):
    product = get_product_by_id(product_id)
    reviews  = get_review_product_id(product_id)
    avg_rev=None
    if reviews:
       avg_rev = round(sum(rev['rating'] for rev in reviews) / len(reviews) if reviews else 1  ,2)

    if request.method == "POST":
  
        flag = insert_review(request)

        if flag:
                
            return redirect("view_product_details" , product_id=product_id)
        
        else: 
            return render(request , "user/product_details.html" ,{"error":1})
    
    else:

        return render(request , "user/product_details.html" ,{"product":product , 
                                                              "reviews":reviews,
                                                              "count_review":len(reviews),
                                                              "avg_review":avg_rev
                                                             })


#cart

def myCart(request):
    if request.method == "GET":
        user_id = request.session.get("user_id",0)

        if not user_id:
            return redirect("user_signin")
        
        cart_items = get_cart_items(user_id)
        
        total_amount = round(sum(item['disscount_price']* item['quantity'] for item in cart_items),2)

        return render(request, "user/mycart.html", {"cart_items": cart_items, "total_amount": total_amount})

def add_cart(request,product_id):
    try:
        user_id = request.session.get("user_id",0)

        if not user_id:
            return redirect("user_signin")
        
        flag = insert_cart(user_id,product_id)

        if flag:
            return redirect("myCart")
        else:
            return render(request, "user/product_details.html",{"error":1})
        
    except Exception as e:
        print("Error in add_cart view: ", e)
        return render(request, "user/product_details.html",{"error":1})

def remove_cart_item(request, cart_id):
    try:
        user_id = request.session.get("user_id", 0)

        if not user_id:
            return redirect("user_signin")

        flag = delete_cart_item(cart_id, user_id)

        if flag:
            return redirect("myCart")
        else:
            return render(request, "user/mycart.html", {"error": 1})

    except Exception as e:
        print("Error in delete_cart_item view: ", e)
        return render(request, "user/mycart.html", {"error": 1})

def update_cart_item(request, cart_id):
    try:
        user_id = request.session.get("user_id", 0)

        if not user_id:
            return redirect("user_signin")
        if request.method == "POST":

            quantity = int(request.POST["qnty"])
            if quantity < 1:
                quantity = 1  # Ensure quantity is at least 1

            flag = update_cart_quantity(cart_id, user_id, quantity)

            if flag:
                return redirect("myCart")
            else:
                return render(request, "user/mycart.html", {"error": 1})
        else:
            return redirect("myCart")

    except Exception as e:
        print("Error in update_cart_item view: ", e)
        return render(request, "user/mycart.html", {"error": 1})


#buy 

def buy_product(request):
    user_id = request.session.get("user_id", 0)
    if not user_id:
        return redirect("user_signin")
    
    if not get_cart_items(user_id=user_id):
            return redirect("index")

    if request.method=="POST":
        
        cart_items = get_cart_items(user_id=user_id)
        flag = buy_cart_items(request ,cart_items)

        if flag :
            return render(request , "user/success.html")
        else:
            return render(request ,'user/buy_product.html',{'error':1})
    else:
        user_details= get_full_details(uid=user_id)

        if  user_details:
            return render(request, "user/buy_product.html",{"user":user_details})
        else:
            return render(request, "user/mycart.html", {"error": 1})    

def myorders(request):
    
    user_id = request.session.get("user_id",0)

    if not user_id :
        return redirect('user_signin')
    
    pending_orders = get_all_orders_by_user_id(user_id=user_id , status='pending')
    delivered_orders = get_all_orders_by_user_id(user_id=user_id , status='delivered')

    return render(request , 'user/myorders.html',{'pending_orders':pending_orders,
                                                  'delivered_orders':delivered_orders})

def cancel_myorder(request,order_id):
    user_id = request.session.get("user_id", 0)
    if not user_id:
        return redirect("user_signin")

    flag = cancel_orders_in_pending(user_id,order_id)

    if flag:
        return redirect('myorders')
    else:
        return render(request,'user/myorders.html',{'error':1})


#chat bot

def chatBot(request):
    try:
        if request.method=="POST":
            user_query = request.POST['user_query']
            products = cb.run(user_query)
            if not products:
                print("No products ")
                return render(request ,'user/index.html',{
                'products':None,
                'user_query':user_query
                })
            
            items=[]
            for product in products:
                items.append( get_product_by_id(product_id=product['product_id']))
            
            products = get_all_products()
            return render(request ,'user/index.html',{
                'chat_items':items,
                'products':products,
                'user_query':user_query
            })
        
        else:
            return redirect('index')

    except Exception as e:
        print("Error in chatBot views.py ",e )
        return redirect('index')


#logout

def logout(request):
    try:
        del request.session["user_id"]
    except KeyError:
        pass
    return redirect("user_signin")