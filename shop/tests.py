from django.test import TestCase
from .models import *
from django.contrib.auth.models import User


class TestOrders(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='hubert.hernoga@wp.pl')
        self.product = Product.objects.create(name='Material 1', price=12.00)
        self.shipping = ShippingOption.objects.create(shipping_method='Post Office', price=7.00)
        self.order = Order.objects.create(user=self.user, shipping_option=self.shipping)
        self.order.save()
        self.order.products.add(self.product)
        self.sale = Sale.objects.create(product=self.product, order=self.order)
        self.sale.save()
        self.order.save()

    def test_order_total_price(self):
        self.assertEqual(self.order.total_price, 19.00)


if __name__ == "__main__":
    unittest.main()
