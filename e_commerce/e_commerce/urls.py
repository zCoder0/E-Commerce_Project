"""
URL configuration for e_commerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from user.urls import *
from inventory.urls import *
from django.conf import settings
from django.conf.urls.static import static

"""
urlpatterns =[
    path('',views.index,name=''),
    path('' ,views.index,name='index'),
]
"""

urlpatterns = [
    path('admin/', admin.site.urls),
]
# Add your user and inventory urls
urlpatterns += user_urlpatterns
urlpatterns += inventory_urlpatterns

# Add media serving (for images)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)