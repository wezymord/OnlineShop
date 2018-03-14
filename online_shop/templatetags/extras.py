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

# @register.filter(name='amount_price_products')
# def amount_price_products(products_amount):
#     total_amount_price = []
#     print(products_amount)
#     for product_id, product_amount in products_amount.items():
#         product = Product.objects.get(pk=product_id)
#         total_amount_price.append(int(product.price) * product_amount)
#     print(total_amount_price)
#     return total_price

@register.filter(name='total_price_basket')
def total_price_basket(products):
    total_price = 0
    for product in products:
        total_price += int(product.price)
    return total_price
