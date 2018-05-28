from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# validators
from django.core.validators import URLValidator
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
# signals
from django.db.models.signals import post_save
from django.dispatch import receiver
# email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# order
import shortuuid, uuid
import datetime

class Product(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    description = models.CharField(max_length=256, null=True)

    def __str__(self):
        return 'name:{} price:{} stock:{} available:{} description{}'\
            .format(self.name, self.price, self.stock, self.available, self.description)


class Photo(models.Model):
    image_urls = models.TextField(validators=[URLValidator()], null=True)
    products = models.ManyToManyField(Product, related_name='photo')

    def __str__(self):
        products = [product.name for product in self.products.all()]
        return ' - '.join(products)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', default=None)
    phone_number = PhoneNumberField(blank=True)
    company = models.CharField(max_length=64, null=True)
    country = CountryField(blank_label='Select country', blank=True)
    city = models.CharField(max_length=64, null=True)
    postal_code = models.CharField(max_length=64, null=True)
    address1 = models.CharField(max_length=64, null=True)
    address2 = models.CharField(max_length=64, null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def update_profile(request, user_id):
        user = User.objects.get(pk=user_id)
        user.save()

class ShippingOption(models.Model):
    shipping_method = models.CharField(max_length=64)
    available_destinations = models.CharField(max_length=64)
    delivery_time = models.CharField(max_length=64)
    delivery_size = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return 'shipping_method:{} available_destinations:{} delivery_time:{} delivery_size:{} price:{}'\
            .format(self.shipping_method, self.available_destinations, self.delivery_time, self.delivery_size, self.price)


order_status = {
    (1, 'Waiting for confirmation'),
    (2, 'Confirmed / Rejected'),
    (3, 'Processing'),
    (4, 'Sent'),
    (5, 'Delivered'),
}


class Order(models.Model):
    uuid = models.CharField(editable=False, max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_user')
    products = models.ManyToManyField(Product, related_name='orders_product')
    shipping_option = models.ForeignKey(ShippingOption, on_delete=models.CASCADE, related_name='orders_shipping_option', null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=30, choices=order_status, default=1)

    def __str__(self):
        return "uuid:{} total_price:{} date:{} status:{}".format(self.uuid, self.total_price, self.date, self.status)

    def save(self, *args, **kwargs):
        self.uuid = shortuuid.encode(uuid.uuid4())
        if self.pk != None:
            product_total = 0
            for product in self.products.all():
                quantity = self.order_sale.get(product_id=product.id).quantity
                product_total += quantity * product.price

            shipping_price = self.shipping_option.price
            total_price = float(product_total) + shipping_price
            self.total_price = total_price
        super(Order, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.active = False
        self.save()


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_sale')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_sale')
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return "quantity:{} price:{}".format(self.quantity, self.price)

    def save(self, *args, **kwargs):
        self.price = self.product.price
        super(Sale, self).save(*args, **kwargs)

    @receiver(post_save, sender=Order)
    def save_order(sender, instance, **kwargs):
        email = User.objects.get(pk=instance.user_id).email

        ctx = {
            'uuid': instance.uuid,
            'base_url': settings.BASE_URL,
        }

        content = render_to_string('email_checkout_complete.html', ctx)
        text_content = strip_tags(content)

        msg = EmailMultiAlternatives(
            subject="Confirmation of purchase Pawel&Marly.com",
            body=text_content,
            from_email="pawelmarlykizomba@gmail.com",
            to=[email])

        msg.attach_alternative(content, "text/html")
        return msg.send()
