from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Product, ShippingOption, Order, OrderProduct
from .forms import UserForm, RegistrationForm
from django.http import QueryDict
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


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
            }

            return render(request, 'index.html', ctx)
        else:
            ctx = {
                'photos': photos,
                'products': products,
            }

            return render(request, 'index.html', ctx)


class AccountOrders(View):
    def get(self, request):
        return render(request, 'account-orders.html')


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

        else:
            ctx = {
                'products': products
            }

        return render(request, 'basket.html', ctx)

    def post(self, request):
        products = request.session.get('basket')
        if products == None:
            products = request.session.get('basket', {})

        product_id = request.POST.get('product_id')
        quantity_product = request.POST.get('quantity_product')
        products[product_id] = quantity_product
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
        quantity_product = QueryDict(request.body).get("quantity_product")
        product_id = QueryDict(request.body).get("product_id")

        if product_id in request.session['basket'].keys():
            del request.session['basket'][product_id]

        products_amount = request.session.get('basket', {})
        products_amount[product_id] = quantity_product
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
    def get(self, request, user_id):
        if user_id:
            logged_user = User.objects.get(pk=user_id)
            logged_user_form = UserForm(user_id=user_id,
                                        initial={
                'first_name': logged_user.first_name,
                'last_name': logged_user.last_name,
                'email': logged_user.email,
                'phone_number': logged_user.profile.phone_number,
                'company': logged_user.profile.company,
                'country': logged_user.profile.country,
                'city': logged_user.profile.city,
                'postal_code': logged_user.profile.postal_code,
                'address1': logged_user.profile.address1,
                'address2': logged_user.profile.address2
            })

            shipping_cost = 0
            if 'shipping' in request.session.keys():
                shipping_id = request.session['shipping']['shipping_method_id']
                shipping = ShippingOption.objects.get(pk=shipping_id)
                shipping_cost += shipping.cost

            ctx = {
                'products_amount': request.session['basket'],
                'logged_user': logged_user.id,
                'user_form': logged_user_form,
                'shipping_cost': format(shipping_cost, '.2f')
            }

        else:
            ctx = {
                'products_amount': request.session['basket'],
                'user_form': UserForm(user_id=user_id),
                'shipping_cost': format(0, '.2f')
            }
        return render(request, 'checkout-address.html', ctx)

    def post(self, request, user_id):
        user_form = UserForm(request.POST or None, user_id=user_id)
        if user_form.is_valid():
            if user_id:
                user = User.objects.get(pk=user_id)
            else:
                user = User(username=user_form.cleaned_data['email'], email=user_form.cleaned_data['email'])
                user.save()
                user = User.objects.get(email=user_form.cleaned_data['email'])

            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.profile.phone_number = user_form.cleaned_data['phone_number']
            user.profile.company = user_form.cleaned_data['company']
            user.profile.country = user_form.cleaned_data['country']
            user.profile.city = user_form.cleaned_data['city']
            user.profile.postal_code = user_form.cleaned_data['postal_code']
            user.profile.address1 = user_form.cleaned_data['address1']
            user.profile.address2 = user_form.cleaned_data['address2']
            user.save()

            return redirect('/checkout_shipping/{}'.format(user.id))
        ctx = {
            'products_amount': request.session['basket'],
            'user_form': user_form,
            'shipping_cost': format(0, '.2f')
        }
        return render(request, 'checkout-address.html', ctx)


class CheckoutShipping(View):
    def get(self, request, user_id):
        shipping_options = ShippingOption.objects.all()
        if 'shipping' in request.session.keys():
            shipping_id = request.session['shipping']['shipping_method_id']
            shipping = ShippingOption.objects.get(pk=shipping_id)

            ctx = {
                'shipping_cost': shipping.cost,
                'user_shipping': shipping,
                'shipping_options': shipping_options,
                'user_id': user_id,
                'products_amount': request.session['basket']

            }
        else:

            ctx = {
                'shipping_options': shipping_options,
                'products_amount': request.session['basket'],
                'user_id': user_id,
                'shipping_cost': format(0, '.2f')
            }

        return render(request, 'checkout-shipping.html', ctx)

    def post(self, request, user_id):
        request.session['shipping'] = dict(request.POST.items())
        shipping = request.session['shipping']
        shipping_id = shipping['shipping_method_id']

        return redirect('/checkout_review/{}/{}'.format(user_id, shipping_id))


class CheckoutReview(View):
    def get(self, request, user_id, shipping_id):
        products = []
        user = User.objects.get(pk=user_id)
        product_ids = request.session['basket']
        for id in product_ids:
            products.append(Product.objects.get(pk=id))

        ctx = {
            'products': list(set(products)),
            'products_amount': request.session['basket'],
            'user': user,
            'shipping_id': shipping_id,
            'shipping_cost': ShippingOption.objects.get(pk=shipping_id).cost
        }

        return render(request, 'checkout-review.html', ctx)

    def post(self, request, user_id, shipping_id):
        product_ids = request.session['basket'].keys()
        user = User.objects.get(pk=user_id)
        shipping = ShippingOption.objects.get(pk=shipping_id)

        make_order = Order(user=user)
        make_order.save()

        for id in product_ids:
            for product in Product.objects.filter(pk=id):
                make_order.products.add(product)
                order_products = OrderProduct(product=product, order=make_order,
                                              quantity_product=request.session['basket'][id])
                order_products.save()

        make_order.shipping_options.add(shipping)

        return redirect('/checkout_complete/{}'.format(make_order.uuid))


class CheckoutComplete(View):
    def get(self, request, uuid):
        ctx = {
            'uuid': uuid
        }

        return render(request, 'checkout-complete.html', ctx)

    def post(self, request, uuid):
        request.session.clear()

        return redirect('/')


class AccountRegistration(View):
    def get(self, request):
        ctx = {
            'user_form': UserForm(user_id=''),
            'registration_form': RegistrationForm()
        }
        return render(request, 'account-registration.html', ctx)

    def post(self, request):
        user_form = UserForm(request.POST, user_id='')
        registration_form = RegistrationForm(request.POST)
        if user_form.is_valid() and registration_form.is_valid():
            user = User.objects.create_user(username=user_form.cleaned_data['email'],
                                            first_name=user_form.cleaned_data['first_name'],
                                            last_name=user_form.cleaned_data['last_name'],
                                            email=user_form.cleaned_data['email'],
                                            password=registration_form.cleaned_data['password'])
            user.save()

            user = User.objects.get(email=user_form.cleaned_data['email'])
            user.profile.phone_number = user_form.cleaned_data['phone_number']
            user.profile.company = user_form.cleaned_data['company']
            user.profile.country = user_form.cleaned_data['country']
            user.profile.city = user_form.cleaned_data['city']
            user.profile.postal_code = user_form.cleaned_data['postal_code']
            user.profile.address1 = user_form.cleaned_data['address1']
            user.profile.address2 = user_form.cleaned_data['address2']
            user.save()

            return redirect('/account_login')

        ctx = {
            'user_form': user_form,
            'registration_form': registration_form
        }
        return render(request, 'account-registration.html', ctx)


class AccountLogin(View):
    def get(self, request):
        return render(request, 'account-login.html')

    def post(self, request):
        user_data = dict(request.POST.items())
        user = authenticate(username=user_data['email'], password=user_data['password'])

        if user:
            login(request, user)
            logged_user = User.objects.get(username=user_data['email'])

            return redirect('/checkout_address/{}'.format(logged_user.id))

        return render(request, 'account-login.html')