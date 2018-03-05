from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Products, Photos

class ProductsList(View):
    def get(self, request):
        products =  Products.objects.all()

        for product in products:
            for url in product.photo.all():
                print(url.image_urls)               # dlaczego wyświetla 3x?


        # images = []
        # for product in products:
        #     images.append(product.image_urls)
        # ctx = {
        #     'images': images
        # }

        return render(request, 'index.html')

class AccountOrders(View):
    def get(self, request):
        pass
        return render(request, 'account-orders.html')


class OrdersBasket(View):
    def get(self, request):
        products = Products.objects.filter(available=True)

        images = []
        for product in products:
            images.append(product.image_urls)
        ctx = {
            'images': images
        }
        return render(request, 'cart.html')