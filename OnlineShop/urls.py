"""OnlineShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path
from online_shop.views import ProductsList, OrdersBasket, ProductDetails, ShowAllProducts

urlpatterns = [
    path('admin/', admin.site.urls),
    url('index/', ProductsList.as_view(), name='index'),
    # url('account_orders/', AccountOrders.as_view(), name='account_orders'),
    url('basket/', OrdersBasket.as_view(), name='basket'),
    url('product_details/(?P<product_id>\d+)', ProductDetails.as_view(), name='product_details'),
    url('show_all_products/', ShowAllProducts.as_view(), name='show_all_products'),

]
