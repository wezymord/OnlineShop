from django.test import TestCase
from .models import *
from django.contrib.auth.models import User
import datetime

class TestOrders(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='hubert.hernoga@wp.pl')
        self.product_1 = Product.objects.create(name='Material 1', price=12.00)
        self.product_2 = Product.objects.create(name='Material 2', price=2.00)
        self.shipping_1 = ShippingOption.objects.create(shipping_method='Post Office', price=7.00)
        self.shipping_2 = ShippingOption.objects.create(shipping_method='Post Office', price=7.00)

    def test_order_total_price_when_quantity_is_0(self):
        self.order = Order.objects.create(user=self.user, shipping_option=self.shipping_1)
        self.order.save()
        self.order.products.add(self.product_1)
        self.sale = Sale.objects.create(product=self.product_1, order=self.order)
        self.sale.save()
        self.order.save()
        self.assertEqual(self.order.total_price, 19.00)

    def test_order_total_price_when_quantity_is_3(self):
        self.order = Order.objects.create(user=self.user, shipping_option=self.shipping_2)
        self.order.save()
        self.order.products.add(self.product_2)
        self.sale = Sale.objects.create(product=self.product_2, order=self.order, quantity=3)
        self.sale.save()
        self.order.save()
        self.assertEqual(self.order.total_price, 13.00)

    def test_order_total_price_when_quantity_is_43(self):
        self.order = Order.objects.create(user=self.user, shipping_option=self.shipping_1)
        self.order.save()
        self.order.products.add(self.product_1)
        self.sale = Sale.objects.create(product=self.product_1, order=self.order, quantity=43)
        self.sale.save()
        self.order.save()
        self.assertEqual(self.order.total_price, 523.00)

    def test_order_date(self):
        self.order = Order.objects.create(user=self.user, shipping_option=self.shipping_1)
        self.order.save()
        self.order.products.add(self.product_1)
        self.sale = Sale.objects.create(product=self.product_1, order=self.order, quantity=43)
        self.sale.save()
        self.order.save()
        self.assertEqual(self.order.date, datetime.date.today())

    def test_order_sale(self):
        self.order = Order.objects.create(user=self.user, shipping_option=self.shipping_1)
        self.order.save()
        self.order.products.add(self.product_1)
        self.sale = Sale.objects.create(product=self.product_1, order=self.order, quantity=43)
        self.sale.save()
        self.order.save()
        for product in self.order.products.all():
            self.assertEqual(product, self.sale.product)

    def test_sale_price_for_product_1(self):
        self.order = Order.objects.create(user=self.user, shipping_option=self.shipping_1)
        self.order.save()
        self.order.products.add(self.product_1)
        self.sale = Sale.objects.create(product=self.product_1, order=self.order, quantity=43)
        self.sale.save()
        self.order.save()
        self.assertEqual(self.sale.price, self.product_1.price)

    def test_sale_price_for_product_2(self):
        self.order = Order.objects.create(user=self.user, shipping_option=self.shipping_1)
        self.order.save()
        self.order.products.add(self.product_2)
        self.sale = Sale.objects.create(product=self.product_2, order=self.order, quantity=43)
        self.sale.save()
        self.order.save()
        self.assertEqual(self.sale.price, self.product_2.price)




if __name__ == "__main__":
    unittest.main()
