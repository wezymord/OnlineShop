from django.db import models
from django.core.validators import URLValidator


class Product(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    description = models.CharField(max_length=256, null=True)

    def __str__(self):
        return '{}'.format(self.name)


class Photo(models.Model):
    image_urls = models.TextField(validators=[URLValidator()], null=True)
    products = models.ManyToManyField(Product, related_name='photo')

    def __str__(self):
        products = []
        for product in self.products.all():
            products.append(product.name)
        return ' - '.join(products)


class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=15)          # validation
    e_mail = models.CharField(max_length=64)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class ShippingOption(models.Model):
    shipping_method = models.CharField(max_length=64)
    available_destinations = models.CharField(max_length=64)
    delivery_time = models.CharField(max_length=64)
    delivery_size = models.CharField(max_length=64)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '{}'.format(self.shipping_method)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_user')
    products = models.ManyToManyField(Product, related_name='orders_product')
    shipping_options = models.ManyToManyField(ShippingOption, related_name='orders_shipping_option')

    def __str__(self):
        shipping_options = []
        for option in self.shipping_options.all():
            shipping_options.append(option.shipping_method)
        return ' - '.join(shipping_options)

