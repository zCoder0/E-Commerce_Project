from e_commerce.database import connect


def add_product(request):
    try:
        sql = "insert into product_details (product_name, price, stock, description, image) values (%s, %s, %s, %s, %s)"
        params = (
            request.POST["product_name"],
            request.POST["price"],
            request.POST["stock"],
            request.POST["description"],
            request.FILES.get("image").name if request.FILES.get("image") else None,
        )

        mycon , mycur = connect()
        mycur.execute(sql, params)
        mycon.commit()
        if mycur.rowcount > 0:
            mycur.close()
            return True
        else:
            mycur.close()
            return False
        
    except Exception as e:
        print(f"Error adding product: {e}")
        return False
    
def get_all_products():
    try:
        sql = "select * from product_details"
        mycon , mycur = connect()
        mycur.execute(sql)
        products = mycur.fetchall()
        mycur.close()
        return products
    
    except Exception as e:
        print(f"Error retrieving products: {e}")
        return []

def get_product_by_id(product_id):
    try:
        sql = "select * from product_details where product_id = %s"
        params = (product_id,)
        mycon , mycur = connect()
        mycur.execute(sql, params)
        product = mycur.fetchone()
        mycur.close()
        return product
    
    except Exception as e:
        print(f"Error retrieving products: {e}")
        return []

def update_product(request,product_id):
    try:
        sql = "update products_details set product_name=%s, price=%s, stock=%s, description=%s, image=%s where product_id=%s"

        params=(
            request.POST['product_name'],
            request.POST['price'],
            request.POST['stock'],
            request.POST['description'],
            request.FILES.get('image').name if request.FILES.get('image') else None,
            product_id
        )

        mycon ,mycur = connect()
        mycur.execute(sql,params)
        mycon.commit()
        if mycur.rowcount > 0:
            mycur.close()
            return True
        else:
            mycur.close()
            return False
        

    except Exception as e:
        print(f"Error updating product: {e}")
        return False

def delete_product(product_id):
    try:
        sql = "delete from product_details where product_id=%s"
        params =(product_id,)

        mycon ,mycur = connect()
        mycur.execute(sql,params)
        mycon.commit()

        if mycur.rowcount > 0:
            mycur.close()
            return True
        else:
            mycur.close()
            return False

    except Exception as e:
        print(f"Error deleting product: {e}")
        return False

    