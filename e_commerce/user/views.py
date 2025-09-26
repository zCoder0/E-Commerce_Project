from django.shortcuts import render,redirect
from user.user_action import *

user_id = None

def index(request):
    user_id =  request.session.get("user_id",0)

    if not user_id:
        return redirect("user_signin")
    
    products = get_all_products()

    product_details = [
        {
            "product_id": product[0],
            "product_name": product[1],
            "description": product[2],
            "price": product[3],
            "offer": product[4],
            "disscount_price": product[3] - (product[3] * product[4] / 100),
            "stock": product[5],
            "image_url": product[11],  # Assuming the image URL is in the second column of product_images
        }
        for product in products
    ]
    print(product_details)
    return render(request , "user/index.html" ,{"products":product_details})

def user_signup(request):

    if request.method == "POST":
        user_name = request.POST['user_name']
        user_email = request.POST['user_email']
        user_password = request.POST['user_password']
        user_mobile = request.POST['user_mobile']

        flag = insert_user_register(user_name= user_name , 
                             user_mobile=user_mobile,
                             user_email=user_email,
                             user_password=user_password)
        
        if flag:
            return redirect("user_signin")
        else:
            return render(request ,"user/user_signup.html",{"error":1})
    else:
        return render(request , "user/user_signup.html")

def user_signin(request):
    if request.method == "POST":
        user_email = request.POST['user_email']
        user_password = request.POST['user_password']

        data = get_user_details(user_email=user_email,
                         user_password = user_password)
        
        if data :
            request.session["user_id"] = data['user_id']
            return redirect("index")
        
        else:
            return render(request ,"user/user_signin.html",{"error":1})
        
    else:
        return render(request , "user/dhuuser_signin.html")
    
def profile(request):

    user_id=  request.session.get("user_id",0)

    if not user_id:
        return redirect("user_signin")
        
    try:
        if request.method == "GET":

            datas = get_full_details(user_id=user_id)

            response_data ={
                "user_id":datas[0],
                "user_name":datas[1],
                "user_email":datas[3],
                "user_mobile":datas[2],
                "address":datas[7],
                "city":datas[8],
                "state":datas[9],
                "zipcode":datas[10],
                "country":datas[11]
            }


            if response_data:
                    return render(request,"user/profile.html",{"user_data":response_data})
            else:
                return render(request,"user/profile.html",{"error":404})
            
        elif request.method =="POST":

            user_id = request.POST['user_id']

            user_name = request.POST['user_name']
            user_email = request.POST['user_email']
            user_mobile = request.POST['user_mobile']

            user_address = request.POST['address']
            user_city = request.POST['city']
            user_state = request.POST['state']
            user_zipcode = request.POST['zipcode']
            user_country = request.POST['country']
            

            flag = update_user_details(user_id=user_id,
                                    address=user_address,
                                city=user_city,
                                state=user_state,
                                zipcode=user_zipcode,
                                country=user_country)

            if flag:
                return redirect("profile")   
            else:
                return render(request ,"user/profile.html",{"error":404}) 
            
    except Exception as e:
        print("Error ",e)
        return None

def myCart(request):
    return render(request,"user/mycart.html")

def view_product_details(request,product_id):
    product = get_product_by_id(product_id)
    reviews  = get_review_product_id(product_id)
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
                                                              "avg_review":avg_rev})

def add_cart(request,product_id):
    return render(request, "user/mycart.html")

def logout(request):
    try:
        del request.session["user_id"]
    except KeyError:
        pass
    return redirect("user_signin")