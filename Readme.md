

**Project setup**
- django-admin startproject E-Commerce
- cd E-Commerce
- django-admin startapp user
- mkdir templates



**Requirements**
- django
- django-admin
- mysql-connector
- mysql


**create Environment**
```sh
python -m venv .venv
```

**Activate Environment**
```sh
python .venv/Scripts/activate.bat
```

**Install Requirements**
```sh
pip install -r requirements.txt
```

**Make migrations**
```sh
python manage.py makemigrations
```

**Run Code**
```sh
python manage.py runserver
```