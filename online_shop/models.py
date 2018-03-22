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
        products = [product.name for product in self.products.all()]
        return ' - '.join(products)


class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    e_mail = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=15)
    company = models.CharField(max_length=64, default=None)
    country = models.CharField(max_length=64, default=None)
    city = models.CharField(max_length=64, default=None)
    postal_code = models.CharField(max_length=64, default=None)
    address1 = models.CharField(max_length=64, default=None)
    address2 = models.CharField(max_length=64, default=None)

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
        shipping_options = [option.shipping_method for option in self.shipping_options.all()]
        return ' - '.join(shipping_options)

    def delete(self, *args, **kwargs):
        self.active = False
        self.save()

class OrderProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity_product = models.CharField(max_length=4)