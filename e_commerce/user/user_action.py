
from user.models import *
from inventory.models import *
from django.db import transaction

#user
def update_user_details(user_id, address, city, state, zipcode, country):
    try:
        # Get the user
        user = UserRegister.objects.get(id=user_id)

        # Get or create details
        details, created = UserDetails.objects.get_or_create(user=user)

        # Update fields
        details.address = address
        details.city = city
        details.state = state
        details.zip_code = zipcode
        details.country = country
        details.save()

        return True
    except UserRegister.DoesNotExist:
        print("User not found")
        return False
    
    except Exception as e:
        print("Error in update_user_details:", e)
        return False
    
def get_full_details(uid):
    try:
        # This will join UserRegister with UserDetails
        user = UserRegister.objects.select_related("details").get(id=uid)
        details = getattr(user, "details", None)

        context = {
            "user_id": user.id,
            "user_name": user.user_name,
            "user_email": user.user_email,
            "user_mobile": user.user_mobile,
            "details_id":details.id if details else 0,
            "address": details.address if details else "",
            "city": details.city if details else "",
            "state": details.state if details else "",
            "zipcode": details.zip_code if details else "",
            "country": details.country if details else "",
        }

        return context
    
    except UserRegister.DoesNotExist:
        print("User not found")
        return None
    
#products
def get_all_products():
    try:
        # Prefetch related images for each product
        products = ProductDetails.objects.prefetch_related("images").all()

        # Convert to list of dictionaries if needed for template
        product_list = []
        for product in products:
            images = " ".join(img.image_url.url if hasattr(img.image_url, 'url') else img.image_url for img in product.images.all())
            product_list.append({
                "product_id": product.id,
                "product_name": product.product_name,
                "description": product.description,
                "price": product.price,
                "offer": product.offer,
                "stock": product.stock,
                "disscount_price": round(product.price-(product.price * product.offer/100),2),
                "images": images,  # list of image URLs
            })

        return product_list

    except Exception as e:
        print(f"Error retrieving products: {e}")
        return []

def get_product_by_id(product_id):
    try:
        # Get the product along with related category, supplier, and images
        product = ProductDetails.objects.select_related("category", "supplier") \
                                        .prefetch_related("images") \
                                        .get(id=product_id)

        # Prepare dictionary to return
        product_data = {
            "product_id": product.id,
            "product_name": product.product_name,
            "description": product.description,
            "price": product.price,
            "offer": product.offer,
            "stock": product.stock,
            "disscount_price": round(product.price-(product.price * product.offer/100),2),
            "images": "".join(img.image_url.url if hasattr(img.image_url, 'url') else img.image_url for img in product.images.all())
        }

        return product_data

    except ProductDetails.DoesNotExist:
        print(f"Product with ID {product_id} does not exist")
        return None
    except Exception as e:
        print(f"Error retrieving product: {e}")
        return None

    except Exception as e:
        print(f"Error retrieving products: {e}")
        return [] 
      
def get_review_product_id(product_id):
    try:
        # Fetch all reviews for the product, joining user & product
        reviews = Reviews.objects.filter(product_id=product_id)\
            .select_related("user", "product")

        review_list = [
            {
                "reviewer": review.user.user_name,  # fetch username from UserRegister
                "comment": review.comment,
                "rating": review.rating,
                "review_date": review.review_date,
            }
            for review in reviews
        ]
        return review_list

    except Exception as e:
        print("Error in get_review_product_id:", e)
        return []

def insert_review(request): 
    try:
        review=Reviews.objects.create(
            user_id = request.session.get("user_id",0),
            product_id = int(request.POST['product_id']),
            comment =   request.POST['comment'],
            rating =  int(request.POST['rating'])
        )
        review.save()
        if review.id:
            return True
        else:
            return False
        
    except Exception  as e:
        print("Error in review ",e)
        return False
    

#cart
def insert_cart(user_id, product_id, quantity=1, status="pending"):
    try:
        cart_id, existing_quantity = is_item_in_cart(user_id, product_id)

        if cart_id:
            # Update the first cart entry
            cart_item = CartDetails.objects.get(id=cart_id)
            cart_item.quantity = existing_quantity + quantity
            cart_item.save()
            # Optionally, delete any duplicate cart entries
            CartDetails.objects.filter(
                user_id=user_id,
                product_id=product_id,
                status='pending'
            ).exclude(id=cart_id).delete()

            return True
        else:
            # Create new cart entry
            cart_item = CartDetails.objects.create(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity,
                status=status
            )
            return True if cart_item.id else False

    except Exception as e:
        print("Error in insert_cart: ", e)
        return False

def is_item_in_cart(user_id, product_id):
    try:
        cart_items = CartDetails.objects.filter(
            user_id=user_id,
            product_id=product_id,
            status='pending'
        )

        if cart_items.exists():
            # Sum all quantities if multiple entries exist
            total_quantity = sum(item.quantity for item in cart_items)
            # Return the first cart item's id (or handle differently if needed)
            return cart_items.first().id, total_quantity
        else:
            return None, 0

    except Exception as e:
        print("Error in is_item_in_cart: ", e)
        return None, 0

def delete_cart_item(cart_id, user_id):
    try:
        deleted, _ = CartDetails.objects.filter(id=cart_id, user_id=user_id, status='pending').delete()
        return deleted > 0
    except Exception as e:
        print("Error in delete_cart_item:", e)
        return False

def get_cart_items(user_id):
    try:
        cart_items = CartDetails.objects.filter(user_id=user_id, status='pending') \
            .select_related('product') \
            .prefetch_related('product__images')

        cart_list = []
        for item in cart_items:
            # Use first image if multiple
            image_url = item.product.images.first().image_url if item.product.images.exists() else "default_image.png"
            disscount_price = item.product.price - (item.product.price * item.product.offer / 100)

            cart_list.append({
                "cart_id": item.id,
                "product_id": item.product.id,
                "product_name": item.product.product_name,
                "description": item.product.description,
                "price": float(item.product.price),
                "offer": item.product.offer,
                "disscount_price": round(disscount_price, 2),
                "stock": item.product.stock,
                "images": image_url,
                "quantity": item.quantity,
                "status": item.status
            })
        
        return cart_list

    except Exception as e:
        print("Error in get_cart_items:", e)
        return []

def update_cart_quantity(cart_id, user_id, quantity):
    try:

        cart_item = CartDetails.objects.get(id=cart_id)
        cart_item.quantity = quantity
        cart_item.save()
        return True

    except Exception as e:
        print("Error in update_cart_quantity ",e)
        return False

def updtae_cart_items_status(user_id,status):
    try:
        update_details = CartDetails.objects.get_or_create(
                user_id=user_id
            )
        update_details.status = status
        update_details.save()
        return True

    except Exception as e:
        print("Error in buy_cart_items: ", e)
        return False


#buy


def buy_cart_items(request, cart_items):
    try:
        shipping_id = request.POST.get('shipping_add')
        payment_method = request.POST.get('payment_method')
        user_id = request.session.get("user_id", 0)

        if not user_id:
            return False

        details = get_shipping_address(shipping_id)

        if not details :
            return False
        
        with transaction.atomic():  # Ensures all inserts succeed or rollback
            for item in cart_items:
                product = ProductDetails.objects.get(id=item['product_id'])
                cart = CartDetails.objects.get(id=item['cart_id'], user_id=user_id)
                order_det = OrderDetails.objects.create(
                    user_id=user_id,
                    product=product,
                    cart=cart,
                    quantity=item['quantity'],
                    total_amount=item['disscount_price'],
                    status='pending',
                    shipping_address=details['address'],
                    shipping_city=details['city'],
                    shipping_state=details['state'],
                    shipping_country=details['country'],
                    shipping_zipcode=details['zipcode'],
                    payment_method=payment_method
                )
                order_det.save()
                if order_det.id:
                    # Optionally mark cart item as purchased
                    cart.status = 'purchased'
                    cart.save()
                else:
                    return False

        return True

    except Exception as e:
        print("Error in buy_cart_items:", e)
        return False

#orders
def get_all_orders_by_user_id(user_id, status="pending"):
    try:
        # Fetch orders for a user with related product and images
        orders = OrderDetails.objects.filter(user_id=user_id, status=status)\
            .select_related('product')\
            .prefetch_related('product__images')  # to get product images efficiently

        order_details = []
        for order in orders:
            image_url = order.product.images.first().image_url if order.product.images.exists() else "default_image.png"
            order_details.append({
                'product_id': order.product.id,
                'product_name': order.product.product_name,
                'images': image_url,
                'product_price': order.total_amount,
                'product_quantity': order.quantity,
                'ordered_date': order.order_date,
                'status': order.status,
                'order_id': order.id
            })

        return order_details

    except Exception as e:
        print("Error in get_all_orders_by_user_id:", e)
        return []

def cancel_orders_in_pending(user_id, order_id):
    try:
        deleted, _ = OrderDetails.objects.filter(
            user_id=user_id, 
            id=order_id, 
            status='pending'
        ).delete()

        return deleted > 0

    except Exception as e:
        print("Error in cancel_orders_in_pending:", e)
        return False

def get_shipping_address(details_id):
    try:
        data = UserDetails.objects.get(
            id=details_id
        )

        if data:
            return {
                'address':data.address,
                'city':data.city,
                'state':data.state,
                'country':data.country,
                'zipcode':data.zip_code,
            }
        else:
            return {}

    except Exception as e:
        print("Error in get shipping address : ",e)
        return False