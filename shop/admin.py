from django.contrib import admin
from .models import Product, Profile, Order, Photo, ShippingOption, OrderProduct
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User



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


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'address1',
                    'postal_code', 'city', 'country', 'is_staff',)
    list_select_related = ('profile',)

    def phone_number(self, instance):
        return instance.profile.phone_number

    def address1(self, instance):
        return instance.profile.address1

    def postal_code(self, instance):
        return instance.profile.postal_code

    def city(self, instance):
        return instance.profile.city

    def country(self, instance):
        return instance.profile.country

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


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


def order_id(obj):
    return obj.order.uuid

class OrderProductsAdmin(admin.ModelAdmin):
    list_display = [order_id, 'product', 'quantity_product']
admin.site.register(OrderProduct, OrderProductsAdmin)




admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)