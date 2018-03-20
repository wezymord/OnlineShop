from django.contrib import admin
from .models import Product, User, Order, Photo, ShippingOption


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'available', 'description']
    list_filter = ['available']
    list_editable = ['price', 'stock', 'available', 'description']
admin.site.register(Product, ProductAdmin)


def products_name(obj):
    products = [product.name for product in obj.products.all()]
    return ' - '.join(products)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['image_urls', products_name]
admin.site.register(Photo, PhotoAdmin)



class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone_number', 'e_mail']
admin.site.register(User, UserAdmin)


def shipping_methods(obj):
    shipping_options = [option.shipping_method for option in obj.shipping_options.all()]
    return ' - '.join(shipping_options)

def product_name(obj):
    products = [product.name for product in obj.products.all()]
    return ' - '.join(products)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', product_name, shipping_methods]
admin.site.register(Order, OrderAdmin)


class ShippingOptionAdmin(admin.ModelAdmin):
    list_display = ['shipping_method', 'delivery_time', 'delivery_size', 'available_destinations', 'cost']
    list_editable = ['delivery_time', 'delivery_size', 'available_destinations', 'cost']
admin.site.register(ShippingOption, ShippingOptionAdmin)
