from django.contrib import admin
from .models import Product, User, Order, Photo


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'available', 'description']
    list_filter = ['available']
    list_editable = ['price', 'stock', 'available']
admin.site.register(Product, ProductAdmin)


def products_name(obj):
    products = []
    for product in obj.products.all():
        products.append(product.name)
    return ' - '.join(products)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['image_urls', products_name]
    list_filter = ['image_urls']
admin.site.register(Photo, PhotoAdmin)



class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone_number', 'e_mail']
    list_filter = ['first_name', 'last_name', 'phone_number', 'e_mail']
admin.site.register(User, UserAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'products']
    list_filter = ['user', 'products']
admin.site.register(Order, OrderAdmin)
