# 🛒 E-Commerce Web Application with Smart Chatbot

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)  
![Django](https://img.shields.io/badge/Django-5.2-green?logo=django&logoColor=white)  
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap&logoColor=white)  
![SQLite](https://img.shields.io/badge/SQLite-3.42-orange?logo=sqlite&logoColor=white)  

---

## 🚀 Overview
This is a **modern e-commerce web application** built with **Django**. Users can browse products, view details, and interact with a **smart chatbot** that recommends products based on user queries.  

The chatbot uses **TF-IDF and cosine similarity** to understand user queries and suggest products with **image, price, offer, and view details button**.  

---

## 🎯 Features

### ✅ User Features
- User login and session management  
- Browse products by categories  
- Product details with image, price, offer, and discount  
- Responsive UI for mobile & desktop  

### 🤖 Chatbot Features
- Floating **chatbot icon** at bottom-right corner  
- Click to open the chat window and type queries  
- Returns **product recommendations** as cards:
  - Product image  
  - Product name  
  - Price & discount  
  - Offer %  
  - “View Details” button  
- Supports natural language queries like:
  - "Show me laptops under 50000"
  - "Any kids toys available?"

### ⚡ Admin / Backend Features
- Products and categories stored in **SQLite database**  
- TF-IDF vectorization for product similarity  
- Price filtering based on user query  
- Structured data for easy chatbot processing  

---

## 🛠️ Technologies Used
- **Backend:** Python 3, Django  
- **Frontend:** HTML5, CSS3, Bootstrap 5, Font Awesome  
- **Database:** SQLite  
- **NLP / Chatbot:** NLTK, TF-IDF, Cosine Similarity  
- **JavaScript:** Chatbot toggle & interactive features  

---


## Project Structure


```graphql
e_commerce/
│
├─ e_commerce/              # Main Django project
├─ inventory/               # Products & categories app
├─ user/                    # User templates and views
├─ media/                   # Uploaded product images
├─ static/                  # CSS, JS, images
├─ templates/               # HTML templates
├─ db.sqlite3               # Database
├─ manage.py                # Django manager
├─ requirements.txt
└─ query.sql
```

---

## 🛠️ Database Setup

### 1. Execute SQL Queries
- All SQL queries for creating tables and inserting data are written in **`query.sql`**.  
- Open MySQL Workbench or terminal and execute the file:

```sql
-- Example using terminal:
mysql -u root -p e_commerce < query.sql
```

Python Database Connection

Connection is handled in e_commerce/database.py

```py
import pymysql

def connect():
    try:
        mycon = pymysql.connect(
            host="127.0.0.1",
            user="root",        # Change this if your MySQL username is different
            password="root",    # Change this if your MySQL password is different
            database="e_commerce"
        )
        mycur = mycon.cursor()
        return mycon, mycur

    except Exception as e:
        print("Database.py Error:", e)
        return None, None

```


## 💻 Installation

1. **Clone repository**
```bash
git clone https://github.com/zCoder0/E-Commerce_Project.git
cd e_commerce


python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

pip install -r requirements.txt


python manage.py makemigrations
python manage.py migrate

python manage.py runserver

```


---
## Inventory Login


  - user name : admin

  - password : admin

---