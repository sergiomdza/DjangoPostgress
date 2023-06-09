"""DjangoPostgres URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from api.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', index_page, name='index_page'),
    path('', home_page, name='home_page'),
    path('product/<int:id>/', product_details, name='product_details'),
    path('product/<int:id>/edit/', edit_product, name='edit_product'),
    path('add_product/', add_product, name='add_product'),
    path('delete_product/<int:id>', delete_product, name='delete_product'),
]
