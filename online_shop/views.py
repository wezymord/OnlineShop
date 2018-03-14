from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Product, Photo
from django.http import QueryDict


class MainPage(View):
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


# class AccountOrders(View):
#     def get(self, request):
#         pass
#         return render(request, 'account-orders.html')


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
        products = request.session.get('basket', [])

        if request.method == 'POST':
            products.append(request.POST.get('product_id'))
            request.session['basket'] = products

        return render(request, 'basket.html')

    def delete(self, request):
        remove_id_product = QueryDict(request.body).get('product_id_remove')
        for id in request.session['basket']:
            if remove_id_product == id:
                request.session['basket'].remove(id)

        request.session.modified = True

        return render(request, 'basket.html')


        #
        # products_amount = request.session.get('products_amount', {})
        # remove_produc = request.session.get('remove_product', [])
        # print(remove_produc)
        # print(request.session.items())
        # if request.method == 'POST':
        #     products_add_list = []
        #     product_id_add = request.POST.get('product_id_add')
        #     products_add_list.append(product_id_add)
        #
        #     remove_produc.append(request.POST.get('product_id_remove'))
        #     print(request.POST.get('product_id_remove'))
        #     request.session['remove_product'] = remove_produc
        #
        #
        #     # for id in products_add_list:
        #     #     product = Product.objects.get(pk=id)
        #     #     products_amount[product.id] = request.POST.get('product_amount')
        # print(remove_produc)
        # print(request.session.items())
        # request.session['products_amount'] = products_amount
        #
        # ctx = {
        #     'products_amount': products_amount
        # }


class ClearBasket(View):
    def get(self, request):
        request.session.clear()
        return redirect('/basket')


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



