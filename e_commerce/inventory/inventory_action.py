from e_commerce.database import connect
import os
from django.conf import settings

#Inventory Actions
def add_product(request):
    try:
        sql = "insert into product_details (product_name, price ,offer, stock, description,category_id,supplier_id) values (%s,%s, %s, %s, %s,%s,%s)"
        params = (
            request.POST["product_name"],
            request.POST["price"],
            request.POST["offer"],
            request.POST["stock"],
            request.POST["description"],
            request.POST['category_id'],
            request.POST['supplier_id']
        )

        mycon , mycur = connect()
        mycur.execute(sql, params)
        mycon.commit()

        flag = True
        image_file = request.FILES.get("product_image")
        if image_file:
                # Save file to MEDIA_ROOT/products/
            image_path = os.path.join(settings.MEDIA_ROOT, "products", image_file.name)

            if search_products(image_file.name):
                return True
            
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            with open(image_path, "wb+") as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            flag = update_product_image(f"media/products/{image_file.name}" , product_id = get_product_id() )

  
        if mycur.rowcount > 0 and flag:
            mycur.close()
            return True
        else:
            mycur.close()
            return False
        
    except Exception as e:
        print(f"Error adding product: {e}")
        return False
    
def update_product_image(image_url , product_id ):
    try:

        sql = "update product_images set image_url=%s where product_id=%s"
      
        params = (image_url,product_id)
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
        print(f"Error adding product image: {e}")
        return False

def search_products(image_name):
    try:
        product_list = os.listdir(os.path.join(settings.MEDIA_ROOT, "products"))

        if image_name in product_list:
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error searching products: {e}")
        return False

def get_product_id():
    try:
        sql = "select max(product_id) from product_details"
        mycon , mycur = connect()
        mycur.execute(sql)

        product_id = mycur.fetchone()[0] 

        mycur.close()
        return product_id
    
    except Exception as e:
        print(f"Error retrieving product id: {e}")
        return None

def get_all_products():
    try:
        sql = "SELECT pd.* , pimg.* FROM product_details pd INNER JOIN product_images pimg on pimg.product_id = pd.product_id;"
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
        sql = """
                SELECT 
                pd.* , pimg.* , cd.category_name , sd.supplier_name
                                
                FROM product_details pd 

                INNER JOIN product_images pimg ON 
                    pimg.product_id = pd.product_id 
                    
                INNER JOIN category_details cd ON
                    cd.category_id = pd.category_id
                    
                INNER JOIN supplier_details sd ON
                    sd.supplier_id = pd.supplier_id
                    
                WHERE pd.product_id=%s
        """
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
        sql = "update products_details set product_name=%s, price=%s,offer=%s, stock=%s, description=%s, image=%s where product_id=%s"

        params=(
            request.POST['product_name'],
            float(request.POST['price']),
            int(request.POST['offer']),
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
          
        image_path = get_product_by_id(product_id)[11]
        sql = "delete from product_details where product_id=%s"
        params =(product_id,)

        mycon ,mycur = connect()
        mycur.execute(sql,params)
        mycon.commit()

        if mycur.rowcount > 0:
            mycur.close()

            if delete_product_image_file(image_path.split('/')[-1]):
                return True
            
            return True
        
        else:
            mycur.close()
            return False

    except Exception as e:
        print(f"Error deleting product: {e}")
        return False

def delete_product_image_file(image_name):
    try:
        image_path = os.path.join(settings.MEDIA_ROOT, "products", image_name)
        if os.path.exists(image_path):
            os.remove(image_path)
            return True
        else:
            print("The file does not exist")
            return False
    except Exception as e:
        print(f"Error deleting product image file: {e}")
        return False

#Category and Supplier Actions
def get_all_categories():
    try:
        sql = "select * from category_details"
        mycon , mycur = connect()
        mycur.execute(sql)
        categories = mycur.fetchall()
        mycur.close()
        return categories
    
    except Exception as e:
        print(f"Error retrieving categories: {e}")
        return []  
    
def get_category_by_id(category_id):
    try:
        sql = "select * from category_details where category_id = %s"
        params = (category_id,)
        mycon , mycur = connect()
        mycur.execute(sql, params)
        category = mycur.fetchone()
        mycur.close()
        return category
    
    except Exception as e:
        print(f"Error retrieving category: {e}")
        return []

def add_category(request):
    try:
        sql = "insert into category_details (category_name, description) values (%s, %s)"
        params = (
            request.POST["category_name"],
            request.POST["description"]
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
        print(f"Error adding category: {e}")
        return False 

def delete_category(category_id):
    try:
        sql = "delete from category_details where category_id=%s"
        params =(category_id,)

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
        print(f"Error deleting category: {e}")
        return False

def update_category(request,category_id):

    try:
        sql = "update category_details set category_name=%s, description=%s where category_id=%s"

        params=(
            request.POST['category_name'],
            request.POST['description'],
            category_id
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
        print(f"Error updating category: {e}")
        return False
    
def get_all_suppliers():
    try:
        sql = "select * from supplier_details"
        mycon , mycur = connect()
        mycur.execute(sql)
        suppliers = mycur.fetchall()
        mycur.close()
        return suppliers
    
    except Exception as e:
        print(f"Error retrieving suppliers: {e}")
        return []
    