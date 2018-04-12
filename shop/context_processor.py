from .models import Product

def basket_summary(request):
    if 'basket' in request.session.keys():
        total_price = 0
        for product_id in list(request.session['basket'].keys()):
            product = Product.objects.get(pk=product_id)
            quantity_product = request.session['basket'][product_id]
            total_price += int(quantity_product) * int(product.price)

        return {
            'display_quantity_products': len(request.session['basket'].keys()),
            'total_basket_price': format(total_price, '.2f')
        }
    else:
        return {
            'display_quantity_products': 0,
            'total_basket_price': format(0, '.2f')
        }


def display_basket(request):
    if 'basket' in request.session.keys():
        products = [Product.objects.get(pk=product_id) for product_id in request.session['basket']]

        return {
            'products_in_basket': list(request.session['basket']),
            'products_amount': request.session['basket'],
            'products_order': products,
        }
    else:
        return {
            'quantity_product': 0
        }
