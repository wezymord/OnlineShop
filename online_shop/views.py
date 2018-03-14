from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Product, Photo


# class ProductsList(View):
#     def get(self, request):
#         products = Product.objects.all()
#         photos = []
#         for product in products:
#             for url in product.photo.all():
#                 photos.append(url.image_urls)
#         ctx = {
#             'photos': photos,
#             'products': products
#         }
#
#         return render(request, 'index.html', ctx)
#
#     def post(self, request):
#         product_id = ''
#         if request.method == 'POST':
#             product_id += request.POST.get('id')
#
#         return redirect('/add_to_basket/{}'.format(product_id))

# class AccountOrders(View):
#     def get(self, request):
#         pass
#         return render(request, 'account-orders.html')


class RequestPostAjax(View):
    def get(self, request):
        products = Product.objects.all()
        photos = []
        for product in products:
            for url in product.photo.all():
                photos.append(url.image_urls)
        ctx = {
            'photos': photos,
            'products': products
        }

        return render(request, 'index.html', ctx)

    def post(self, request):
        products = request.session.get('basket', [])

        if request.method == 'POST':
            products.append(request.POST.get('product_id'))
            request.session['basket'] = products
        print(request.session.items())
        return render(request, 'index.html')


class Basket(View):
    def get(self, request):
        products = []
        if request.session.items():
            products_id = request.session['basket']
            for id in products_id:
                products.append(Product.objects.get(pk=id))

            ctx = {
                'products': products
            }

            return render(request, 'basket.html', ctx)
        else:
            ctx = {
                'products': products
            }

            return render(request, 'basket.html', ctx)

    def post(self, request):
        products_amount = request.session.get('products_amount', {})

        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            products_id_list = []
            products_id_list.append(product_id)

            for id in products_id_list:
                product = Product.objects.get(pk=id)
                products_amount[product.id] = request.POST.get('product_amount')

        request.session['products_amount'] = products_amount
        print(products_amount)
        ctx = {
            'products_amount': products_amount
        }
        return render(request, 'basket.html', ctx)


class ProductDetails(View):
    def get(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        photos = product.photo.all()

        ctx = {
            'product': product,
            'photos': photos
        }
        return render(request, 'shop-single.html', ctx)


class ShowAllProducts(View):
    def get(self, request):
        products = Product.objects.all()

        ctx = {
            'products': products
        }
        return render(request, 'shop-grid-ns.html', ctx)

class ClearBasket(View):
    def get(self, request):
        request.session.clear()
        return redirect('/basket')
