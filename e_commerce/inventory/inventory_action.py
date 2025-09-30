
import os
from django.conf import settings
from inventory.models import *
#Inventory Actions
from django.shortcuts import get_object_or_404
from django.conf import settings
import os

from django.db.models import Sum, Count


def add_product(request):
    try:
        # 1️⃣ Create product with category and supplier references
        product = ProductDetails.objects.create(
            product_name=request.POST["product_name"],
            price=request.POST["price"],
            description=request.POST["description"],
            offer=request.POST["offer"],
            stock=request.POST["stock"],
            category_id=request.POST["category_id"],   # OK because _id accepts raw ID
            supplier_id=request.POST["supplier_id"],   # supplier_id instead of supplier
        )

        # 2️⃣ Handle product image
        image_file = request.FILES.get("product_image")

        if image_file:
            # Save file to media/products/
            image_dir = os.path.join(settings.MEDIA_ROOT, "products")
            os.makedirs(image_dir, exist_ok=True)

            image_path = os.path.join(image_dir, image_file.name)
            with open(image_path, "wb+") as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)

            # Save relative path to DB
            ProductImages.objects.create(
                product=product,
                image_url=f"products/{image_file.name}"
            ).save()

        else:
            # Fallback to default image
            ProductImages.objects.create(product=product)

        return True if product.id else False

    except Exception as e:
        print(f"Error adding product: {e}")
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
                "category_id": product.category.id if product.category else None,
                "supplier_id": product.supplier.id if product.supplier else None,
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
            "disscounted_price": round(product.price-(product.price * product.offer/100),2),
            "category_name": product.category.category_name if product.category else None,
            "supplier_name": product.supplier.supplier_name if product.supplier else None,
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

def update_product(request, product_id):
    try:
        product = ProductDetails.objects.get(id=product_id)
        product.product_name = request.POST['product_name']
        product.price = float(request.POST['price'])
        product.offer = int(request.POST['offer'])
        product.stock = int(request.POST['stock'])
        product.description = request.POST['description']
        product.save()
        return True
    except ProductDetails.DoesNotExist:
        print("Product not found.")
        return False
    except Exception as e:
        print(f"Error updating product: {e}")
        return False

def delete_product(product_id):
    try:
        product = ProductDetails.objects.get(id=product_id)
        
        # get related image (if exists)
        product_image = ProductImages.objects.filter(product=product).first()
        if product_image and product_image.image_url:
            image_path = os.path.join(settings.MEDIA_ROOT, product_image.image_url)
            if os.path.exists(image_path):
                os.remove(image_path)  # delete file from disk
        product.delete()  # will also delete related ProductImages if you set CASCADE
        return True
    
    except ProductDetails.DoesNotExist:
        print("Product not found.")
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
        categories = CategoryDetails.objects.all()
        category_list = [
            {
                "id": cat.id,
                "category_name": cat.category_name,
                "description": cat.description
            }
            for cat in categories
        ]
        return category_list
    except Exception as e:
        print(f"Error retrieving categories: {e}")
        return []
    
def get_category_by_id(category_id):
    try:

        category = CategoryDetails.objects.get(id=category_id)
        category_details = {
            "category_id": category.id,
            "category_name": category.category_name,
            "description": category.description,
        }
        return category_details
    
    except Exception as e:
        print(f"Error retrieving category: {e}")
        return []

def add_category(request):
    try:
        category = CategoryDetails.objects.create(
            category_name = request.POST["category_name"],
            description = request.POST["description"]
        )
        category.save()

        if category.id:
            return True
        else:
            return False
        
    except Exception as e:
        print(f"Error adding category: {e}")
        return False 

def delete_category(category_id):
    try:
        category = CategoryDetails.objects.get(id=category_id)  # returns a single instance
        category.delete()  # works correctly
        return True
    except CategoryDetails.DoesNotExist:
        print("Category not found")
        return False
    except Exception as e:
        print(f"Error deleting category: {e}")
        return False

def update_category(request,category_id):
    try:
        category, created = CategoryDetails.objects.get_or_create(id = category_id)
        category.category_name = request.POST['category_name']
        category.description = request.POST['description']
        category.save()

        if category.id:

            return True
        else:
            return False
        
    except Exception as e:
        print(f"Error updating category: {e}")
        return False
    

#supplier 

def get_all_suppliers():
    try:
        suppliers = SupplierDetails.objects.all()

        supplier_details=[
            {
                'supplier_id':supplier.id,
                'supplier_name':supplier.supplier_name,
                'supplier_contact':supplier.contact_name,
                'supplier_mobile':supplier.phone ,
                'address':supplier.address,
                'city':supplier.city,
                'country':supplier.country,
                'zipcode':supplier.postal_code,
                'state':supplier.state,
            }
            for supplier in suppliers
        ]
        return supplier_details
    except Exception as e:
        print(f"Error retrieving suppliers: {e}")
        return []

def get_supplier_by_id(supplier_id):
    try:
        supplier = SupplierDetails.objects.get(id=supplier_id)
        return supplier  # returns a SupplierDetails object
    except SupplierDetails.DoesNotExist:
        print("Supplier not found")
        return None
    except Exception as e:
        print(f"Error retrieving supplier: {e}")
        return None

def add_supplier_details(request):
    try:
        supplier  = SupplierDetails.objects.create(
            supplier_name=request.POST['supplier_name'],
            contact_name=request.POST['supplier_contact_name'],
            address=request.POST['address'],
            city=request.POST['city'],
            postal_code=request.POST['zipcode'],
            country=request.POST['country'],
            phone=request.POST['mobile'],
            state = request.POST['state']
        )
        supplier.save()

        if supplier.id:
            return True
        
        return False
    except Exception as e:
        print("Error in add supplier details:", e)
        return False

def update_supplier(request, supplier_id):
    try:
        supplier = SupplierDetails.objects.get(id=supplier_id)
        supplier.supplier_name = request.POST['supplier_name']
        supplier.contact_name = request.POST['supplier_contact_name']
        supplier.address = request.POST['address']
        supplier.city = request.POST['city']
        supplier.postal_code = request.POST['zipcode']
        supplier.country = request.POST['country']
        supplier.phone = request.POST['mobile']
        supplier.state = request.POST['state']
        supplier.save()
        return True
    
    except SupplierDetails.DoesNotExist:
        print("Supplier not found")
        return False
    
    except Exception as e:
        print("Error in update supplier:", e)
        return False
    
def delete_supplier(supplier_id):
    try:
        supplier = SupplierDetails.objects.get(id=supplier_id)
        supplier.delete()
        return True
    except SupplierDetails.DoesNotExist:
        print("Supplier not found")
        return False
    except Exception as e:
        print("Error in delete supplier:", e)
        return False


#Stock level

def get_all_stock():
    try:
        stocks = ProductDetails.objects.values(
            'product_name',
            'category__category_name',
            'supplier__supplier_name',
            'supplier__address'
        ).annotate(
            total_stock=Sum('stock'),
            total_products=Count('id')
        ).order_by('-total_stock')

        stock_details = [
            {
                "product_name": stock['product_name'],
                "category_name": stock['category__category_name'],
                "supplier_name": stock['supplier__supplier_name'],
                "address": stock['supplier__address'],
                "total_stock": stock['total_stock'],
                "total_products": stock['total_products']
            }
            for stock in stocks
        ]

        return stock_details

    except Exception as e:
        print(f"Error in get_all_stock_orm: {e}")
        return []

def get_stock_by_category(category_id):
    try:
        stocks = ProductDetails.objects.filter(category_id=category_id).values(
            'product_name',
            'category__category_name',
            'supplier__supplier_name',
            'supplier__address'
        ).annotate(
            total_stock=Sum('stock'),
            total_products=Count('id')
        ).order_by('-total_stock')

        stock_details = [
            {
                "product_name": stock['product_name'],
                "category_name": stock['category__category_name'],
                "supplier_name": stock['supplier__supplier_name'],
                "address": stock['supplier__address'],
                "total_stock": stock['total_stock'],
                "total_products": stock['total_products']
            }
            for stock in stocks
        ]

        return stock_details

    except Exception as e:
        print(f"Error in get_stock_by_category_orm: {e}")
        return []
