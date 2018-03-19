from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Product, ShippingOption
from django.http import QueryDict


class MainPage(View):
    def get(self, request):
        products = Product.objects.all()
        photos = []
        for product in products:
            for url in product.photo.all():
                photos.append(url.image_urls)

        if 'basket' in request.session.keys():
            ctx = {
                'photos': photos,
                'products': products,
                'products_amount': request.session['basket']
            }

            return render(request, 'index.html', ctx)
        else:
            ctx = {
                'photos': photos,
                'products': products,
            }

            return render(request, 'index.html', ctx)


# class AccountOrders(View):
#     def get(self, request):
#         pass
#         return render(request, 'account-orders.html')


class Basket(View):
    def get(self, request):
        products = []
        if 'basket' in request.session.keys():
            products_id = request.session['basket']
            for id in products_id:
                products.append(Product.objects.get(pk=id))

            ctx = {
                'products': list(set(products)),
                'products_amount': request.session['basket']
            }

            return render(request, 'basket.html', ctx)
        else:
            ctx = {
                'products': products
            }
            return render(request, 'basket.html', ctx)

    def post(self, request):
        products = request.session.get('basket', {})

        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            product_amount = request.POST.get('product_amount')
            products[product_id] = product_amount
            request.session['basket'] = products

        return render(request, 'basket.html')

    def delete(self, request):
        remove_id_product = QueryDict(request.body).get('product_id')

        for id in list(request.session['basket'].keys()):
            if remove_id_product == id:
                del request.session['basket'][id]

        request.session.modified = True

        return render(request, 'basket.html')

    def put(self, request):
        product_amount = QueryDict(request.body).get("product_amount")
        product_id = QueryDict(request.body).get("product_id")

        if product_id in request.session['basket'].keys():
            del request.session['basket'][product_id]

        products_amount = request.session.get('basket', {})
        products_amount[product_id] = product_amount
        request.session['basket'] = products_amount

        return render(request, 'basket.html')


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

class CheckoutAddress(View):
    def get(self, request):
        pass
        return render(request, 'checkout-address.html')


class CheckoutShipping(View):
    def get(self, request):
        shipping_options = ShippingOption.objects.all()

        ctx = {
            'shipping_options': shipping_options
        }

        return render(request, 'checkout-shipping.html', ctx)


class CheckoutReview(View):
    def get(self, request):
        products = []
        if 'basket' in request.session.keys():
            products_id = request.session['basket']
            for id in products_id:
                products.append(Product.objects.get(pk=id))

            ctx = {
                'products': list(set(products)),
                'products_amount': request.session['basket']
            }

            return render(request, 'checkout-review.html', ctx)
        else:
            return render(request, 'checkout-review.html')

    def post(self, request):
        pass
        return render(request, 'checkout-review.html')


class CheckoutComplete(View):
    def get(self, request):
        pass
        return render(request, 'checkout-complete.html')