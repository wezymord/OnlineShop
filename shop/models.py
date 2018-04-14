from django.db import models
import uuid
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
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '{}'.format(self.shipping_method)


class Order(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_user')
    products = models.ManyToManyField(Product, related_name='orders_product')
    shipping_options = models.ManyToManyField(ShippingOption, related_name='orders_shipping_option')

    def __str__(self):
        shipping_options = [option.shipping_method for option in self.shipping_options.all()]
        return ' - '.join(shipping_options)

    def delete(self, *args, **kwargs):
        self.active = False
        self.save()

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity_product = models.CharField(max_length=4)

    @receiver(post_save, sender=Order)
    def save_order(sender, instance, **kwargs):
        email = User.objects.get(pk=instance.user_id).email
        content = render_to_string('email_checkout_complete.html', {'uuid': instance.uuid})
        text_content = strip_tags(content)
        msg = EmailMultiAlternatives(
            subject="Confirmation of purchase Pawel&Marly.com",
            body=text_content,
            from_email="pawelmarlykizomba@gmail.com",
            to=[email])
        msg.attach_alternative(content, "text/html")
        return msg.send()
