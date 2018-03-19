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
from online_shop.views import MainPage, Basket, ProductDetails, ShowAllProducts, ClearBasket, CheckoutAddress, \
    CheckoutShipping, CheckoutReview, CheckoutComplete


urlpatterns = [
    path('admin/', admin.site.urls),
    url('main_page/', MainPage.as_view(), name='main_page'),
    url('show_all_products/', ShowAllProducts.as_view(), name='show_all_products'),
    url('product_details/(?P<product_id>\d+)', ProductDetails.as_view(), name='product_details'),
    url('basket/', Basket.as_view(), name='basket'),
    url('basket/(?P<product_id>\d+)', Basket.as_view(), name='basket'),
    url('clear_basket_session/', ClearBasket.as_view(), name='clear_basket_session'),
    url('checkout_address/', CheckoutAddress.as_view(), name='checkout_address'),
    url('checkout_shipping/', CheckoutShipping.as_view(), name='checkout_shipping'),
    url('checkout_review/', CheckoutReview.as_view(), name='checkout_review'),
    url('checkout_complete/', CheckoutComplete.as_view(), name='checkout_complete'),
    # url('index/', ProductsList.as_view(), name='index'),
    # url('account_orders/', AccountOrders.as_view(), name='account_orders'),





]
