from django.contrib import admin
from .models import Products, Users, Orders


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'available', 'description']
    list_filter = ['available']
    list_editable = ['price', 'stock', 'available']
admin.site.register(Products, ProductAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone_number', 'e_mail']
    list_filter = ['first_name', 'last_name', 'phone_number', 'e_mail']
admin.site.register(Users, UserAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'products']
    list_filter = ['user', 'products']
admin.site.register(Orders, OrderAdmin)
