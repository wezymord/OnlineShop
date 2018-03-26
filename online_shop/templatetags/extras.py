from django import template
from ..models import Product

register = template.Library()

@register.filter(name='get_title_photo')
def get_title_photo(product):
    photos = product.photo.all()
    photo = []
    for url in photos:
        photo.append(url.image_urls)
    return photo[0]

@register.filter(name='get_stock_product_to_basket')
def get_stock_product_to_basket(product_stock):
    return range(1, product_stock+1)

@register.filter(name='get_product_quantity')
def get_product_quantity(products_amount, product_id):
    for id, amount in products_amount.items():
        if product_id == int(id):
            return int(products_amount[id])

@register.filter(name='get_price_product')
def get_price_product(products_amount, product_id):
    product_price = 0
    for id in products_amount:
        if product_id == int(id):
            product = Product.objects.get(pk=id)
            product_price += int(products_amount[id]) * int(product.price)
    return product_price

@register.filter(name='total_price_basket')
def get_total_price(products_amount):
    total_price = 0
    for id in products_amount:
        product = Product.objects.get(pk=id)
        total_price += int(products_amount[id]) * int(product.price)
    return total_price

@register.filter(name='total_shipping_price')
def total_shipping_price(products_amount, shipping_cost):
    total_price = get_total_price(products_amount)
    total_price += int(shipping_cost)

    return total_price