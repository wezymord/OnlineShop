from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import LoginForm
from .models import Products

class ProductsList(View):
    def get(self, request):
        products =  Products.objects.filter(available=True)

        images = []
        for product in products:
            images.append(product.image_urls)
        ctx = {
            'images': images
        }

        return render(request, 'index.html', ctx)

class AccountOrders(View):
    def get(self, request):
        pass
        return render(request, 'account-orders.html')

