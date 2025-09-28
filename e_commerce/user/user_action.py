from e_commerce.database import connect


def insert_user_register(user_name:str,user_mobile:str, user_email:str ,user_password:str):
    try:
        sql = "insert into user_register (user_name ,user_mobile , user_email , user_password )values(%s ,%s,%s,%s)"
        val = (user_name ,user_mobile ,user_email , user_password )

        mycon , mycur = connect()

        mycur.execute(sql,val)
        mycon.commit()

        if mycur.rowcount:
            return True
        else:
            return False

    except Exception as e:
        print("Error ",e)
        return None 

def get_user_details(user_email,user_password):
    try:
        sql = "select * from  user_register where user_email =%s and user_password = %s"
        val = (user_email , user_password)

        mycon ,mycur = connect()
        mycur.execute(sql,val)
        datas= mycur.fetchone()
        response_data ={
            "user_id":datas[0],
            "user_name":datas[1],
            "user_email":datas[3],
            "user_mobile":datas[2]
        } 

        return response_data
    
    except Exception as e:
        print("User_action.py Error line of 9 : ",e)
        return None
    
def update_user_details(address, city, state, zipcode ,country ,user_id=None):
    try:
        sql = "update user_details set address = %s , city=%s , state = %s , zip_code = %s , country =%s where user_id =%s"
        val=(address , city, state , zipcode ,country ,user_id)

        mycon , mycur = connect()

        mycur.execute(sql,val)
        mycon.commit()
        return True
    
    except Exception as e:
        print("Error in update_user_details : ",e)
        return None

def get_full_details(user_id):
    try:
        sql="""
            select ur.*  , ud.* from user_register ur inner join user_details ud on ud.user_id = ur.user_id where ur.user_id=%s
        """
        val = (user_id,)

        mycon ,mycur =connect()

        mycur.execute(sql,val)
        data = mycur.fetchall()
        return data
    
    except Exception as e:
        print("Error ",e)
        return None

def get_all_products():
    try:
        sql="""
             SELECT 
                pd.product_id, 
                pd.product_name, 
                pd.description,
                pd.price,
                pd.offer,
                pd.price - (pd.price * pd.offer/100 ) AS disscount_price,
                pd.stock,
                pimg.image_url

            FROM product_details pd
            INNER JOIN product_images pimg
                ON pd.product_id = pimg.product_id

        """
        mycon , mycur = connect()
        mycur.execute(sql)
        products = mycur.fetchall()

        product_list = [ { 
                "product_id": product[0],
                "product_name": product[1],
                "description": product[2],
                "price": product[3],
                "offer": product[4],
                "disscount_price": round(product[5],2),
                "stock": product[6],
                "image_url": product[7],  # Assuming the image URL is in the second column of product_images
        } for product in products]

        mycur.close()
        return product_list
    
    except Exception as e:
        print("Error in get_all_products : ",e)
        return None

def get_product_by_id(product_id):
    try:
        sql = """
            SELECT 
                pd.product_id, 
                pd.product_name, 
                pd.description,
                pd.price,
                pd.offer,
                pd.price - (pd.price * pd.offer/100 ) AS disscount_price,
                pd.stock,
                pimg.image_url

            FROM product_details pd
            INNER JOIN product_images pimg
                ON pd.product_id = pimg.product_id

            WHERE pd.product_id = %s
        """
        params = (product_id,)
        mycon, mycur = connect()
        mycur.execute(sql,params)
        product = mycur.fetchone()
        mycur.close()

        product_list = {
                "product_id": product[0],
                "product_name": product[1],
                "description": product[2],
                "price": product[3],
                "offer": product[4],
                "disscount_price": product[5],
                "stock": product[6],
                "image_url": product[7],   # Assuming the image URL is in the second column of product_images
        }
           

        return product_list
    
    except Exception as e:
        print("Error in get_all_products_with_review : ", e)
        return None
    
def get_review_product_id(product_id):
    try:
        sql = """
            SELECT 
                ur.user_name,
                r.`comment` ,
                r.rating,
                r.review_date
                
            FROM product_details pd

            inner JOIN reviews r
                ON r.product_id = pd.product_id
                
            inner JOIN user_register ur
                ON ur.user_id = r.user_id
                
            WHERE pd.product_id = %s


        """
        params = (product_id,)
        mycon, mycur = connect()
        mycur.execute(sql,params)
        reviews = mycur.fetchall()
        mycur.close()

        review_list = [{
                "reviewer": review[0],
                "comment": review[1],
                "rating": review[2],
                "review_date": review[3],  # Assuming the image URL is in the second column of product_images
        } for review in reviews]
           
        return review_list
    
    except Exception as e:
        print("Error in get_all_products_with_review : ", e)
        return None
    
def insert_review(request): 
    try:
        sql ="insert into reviews (user_id , product_id , `comment` , rating) values (%s ,%s ,%s ,%s)"
        params =(
            request.session.get("user_id",0),
            int(request.POST['product_id']),
            request.POST['comment'],
            int(request.POST['rating'])
        )
        mycon , mycur = connect()
        mycur.execute(sql,params)
        mycon.commit()
        if mycur.rowcount:
            return True
        else:
            return False
        
    except Exception  as e:
        print("Error in review ",e)
        return False
    
def insert_cart(user_id, product_id, quantity=1 , status="pending"):

    try:
        sql = """
            INSERT INTO cart_details (user_id, product_id, quantity ,status)
            VALUES (%s, %s, %s,%s)
            ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity)
        """

        cart_id , qnty = is_item_in_cart(user_id, product_id)

        if qnty:
            return update_cart_quantity(cart_id=cart_id, user_id=user_id, quantity=qnty + quantity)
        
          # If the item is already in the cart, we don't want to add more quantity here

        params = (user_id, product_id, quantity,status)

        mycon, mycur = connect()
        mycur.execute(sql, params)
        mycon.commit()

        if mycur.rowcount:
            return True
        else:
            return False

    except Exception as e:
        print("Error in add_to_cart: ", e)
        return False
    
def delete_cart_item(cart_id ,user_id):
    try:
        sql = "DELETE FROM cart_details WHERE cart_id = %s and user_id=%s"
        params = (cart_id,user_id)

        mycon, mycur = connect()
        mycur.execute(sql, params)
        mycon.commit()

        if mycur.rowcount:
            return True
        else:
            return False

    except Exception as e:
        print("Error in delete_cart_item: ", e)
        return False

def get_cart_items(user_id):
    try:
        sql = """
            SELECT 
                cd.cart_id,
                pd.product_id,
                pd.product_name,
                pd.description,
                pd.price,
                pd.offer,
                pd.price - (pd.price * pd.offer/100 ) AS disscount_price,
                pd.stock,
                pimg.image_url,
                cd.quantity,
                cd.status
            
            FROM cart_details cd
            INNER JOIN product_details pd ON cd.product_id = pd.product_id
            INNER JOIN product_images pimg ON pd.product_id = pimg.product_id
            WHERE cd.user_id = %s AND cd.status = 'pending'
        """
        params = (user_id,)

        mycon, mycur = connect()
        mycur.execute(sql, params)
        cart_items = mycur.fetchall()
        mycur.close()

        cart_list = [{
                "cart_id": item[0],
                "product_id": item[1],
                "product_name": item[2],
                "description": item[3],
                "price": item[4],
                "offer": item[5],
                "disscount_price": round(item[6],2),
                "stock": item[7],
                "image_url": item[8],   # Assuming the image URL is in the second column of product_images
                "quantity": item[9],
                "status":item[10]
        } for item in cart_items]
    
        return cart_list
    
    except Exception as e:
        print("Error in get_cart_items : ", e)
        return None

def update_cart_quantity(cart_id, user_id, quantity):
    try:
        sql = "UPDATE cart_details SET quantity = %s WHERE cart_id = %s AND user_id = %s"
        params = (quantity, cart_id, user_id)

        mycon, mycur = connect()
        mycur.execute(sql, params)
        mycon.commit()

        if mycur.rowcount:
            return True
        else:
            return False

    except Exception as e:
        print("Error in update_cart_quantity: ", e)
        return False

def is_item_in_cart(user_id, product_id):
    try:
        sql = "SELECT cart_id , quantity FROM cart_details WHERE user_id = %s AND product_id = %s AND status = 'pending'"
        params = (user_id, product_id)

        mycon, mycur = connect()
        mycur.execute(sql, params)
        item = mycur.fetchone()
        mycur.close()

        if item:

            return item
        else:
            return False,False

    except Exception as e:
        print("Error in is_item_in_cart: ", e)
        return False,False

def updtae_cart_items_status(user_id):
    try:
        sql = "UPDATE cart_details SET status = 'ordering' WHERE user_id = %s AND status = 'pending'"
        params = (user_id,)

        mycon, mycur = connect()
        mycur.execute(sql, params)
        mycon.commit()

        if mycur.rowcount:
            return True
        else:
            return False

    except Exception as e:
        print("Error in buy_cart_items: ", e)
        return False

def buy_cart_items(request , cart_items):
    try:
        shipping_id = request.POST['shipping_add']
        payment_method = request.POST['payment_method']
        user_id = request.session.get("user_id",0)
        
        details = get_shipping_address(shipping_id)

        sql = """insert  into order_details (user_id , product_id ,cart_id ,quantity ,
                                                total_amount ,status,shipping_address ,shipping_city , 
                                                shipping_state ,shipping_country ,shipping_zipcode,payment_method)
                                                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                                 """
        
        params=[]
        for items in cart_items:
            product_id = items['product_id']
            cart_id = items['cart_id']
            quantity = items['quantity']
            total_amount = items['disscount_price']

            params.append((user_id , product_id , cart_id ,quantity , total_amount, "pending" , details['shipping_address'] ,
                details['shipping_city'] ,details['shipping_state'] ,details['shipping_country'] ,details['shipping_zipcode'],payment_method))
            
       
        mycon,mycur =connect()

        mycur.executemany(sql,params)
        mycon.commit()

        if mycur.rowcount>0:
            return True
        else:
            return False

    except Exception as e:
        print("Error in buy cart items : ",e)
        return False

def get_all_orders_by_user_id(user_id,status="pending"):
    try:
        sql="""
            SELECT 
		od.product_id,
		pd.product_name,
		pimg.image_url,
		od.quantity,
		od.total_amount,
		od.order_date,
		od.`status`,
		od.order_id

            from order_details od 

            inner join product_details pd on

                pd.product_id = od.product_id

            inner join product_images pimg on

                pimg.product_id = od.product_id
            
            where od.user_id =%s AND od.status=%s

             
            """
        params=(
            user_id , status 
        )

        mycon,mycur= connect()

        mycur.execute(sql,params)
        orders = mycur.fetchall()

        order_details=[
            {
                'product_id':order[0],
                'product_name':order[1],
                'image_url':order[2],
                'product_price':order[4],
                'product_quantity':order[3],
                'ordered_date':order[5],
                'status':order[6],
                'order_id':order[7]
            }
            for order in orders
        ]
        return order_details
    except Exception as e:
        print("Error in get all orders by user id : ",e)
        return False

def cancel_oders_in_pending(user_id,order_id,status='pending'):
    try:
        sql = "delete from order_details where user_id=%s and status=%s and order_id=%s"
        params=(
            user_id,status,order_id
        )

        print(params)
        mycon ,mycur = connect()
        mycur.execute(sql,params)
        mycon.commit()

        if mycur.rowcount>0:
            return True
        else:
            return False
        
    except Exception as e:
        print("Error in cancel orders in pending : ",e)
        return False

def get_shipping_address(details_id):
    try:
        sql = "select * from user_details where details_id=%s"
        params=(details_id,)

        mycon ,mycur = connect()
        mycur.execute(sql,params)
        data = mycur.fetchone()

        if data:
            return {
                'shipping_address':data[2],
                'shipping_city':data[3],
                'shipping_state':data[4],
                'shipping_country':data[6],
                'shipping_zipcode':data[5],
            }
        else:
            return False

    except Exception as e:
        print("Error in get shipping address : ",e)
        return False