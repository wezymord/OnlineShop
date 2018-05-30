from django.test import TestCase
from ...models import *
from django.contrib.auth.models import User
import datetime

class TestOrders(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='huberth@wp.pl')
        self.product_1 = Product.objects.create(name='Material 1', price=12.00)
        self.product_2 = Product.objects.create(name='Material 2', price=2.00)
        self.shipping_1 = ShippingOption.objects.create(shipping_method='Post Office', price=7.00)
        self.shipping_2 = ShippingOption.objects.create(shipping_method='Post Office', price=7.00)

    def test_order_total_price_when_quantity_is_0(self):
        order = Order.objects.create(user=self.user, shipping_option=self.shipping_1)
        order.products.add(self.product_1)
        Sale.objects.create(product=self.product_1, order=order)
        order.save()
        self.assertEqual(order.total_price, 19.00)

    def test_order_total_price_when_quantity_is_3(self):
        order = Order.objects.create(user=self.user, shipping_option=self.shipping_2)
        order.products.add(self.product_2)
        Sale.objects.create(product=self.product_2, order=order, quantity=3)
        order.save()
        self.assertEqual(order.total_price, 13.00)

    def test_order_total_price_when_quantity_is_43(self):
        order = Order.objects.create(user=self.user, shipping_option=self.shipping_1)
        order.products.add(self.product_1)
        Sale.objects.create(product=self.product_1, order=order, quantity=43)
        order.save()
        self.assertEqual(order.total_price, 523.00)

    def test_order_date(self):
        order = Order.objects.create(user=self.user, shipping_option=self.shipping_1)
        order.products.add(self.product_1)
        Sale.objects.create(product=self.product_1, order=order, quantity=43)
        order.save()
        self.assertEqual(order.date, datetime.date.today())

    def test_order_sale(self):
        order = Order.objects.create(user=self.user, shipping_option=self.shipping_1)
        order.products.add(self.product_1)
        sale = Sale.objects.create(product=self.product_1, order=order, quantity=43)
        order.save()
        for product in order.products.all():
            self.assertEqual(product, sale.product)

    def test_sale_price_for_product_1(self):
        order = Order.objects.create(user=self.user, shipping_option=self.shipping_1)
        order.products.add(self.product_1)
        sale = Sale.objects.create(product=self.product_1, order=order, quantity=43)
        order.save()
        self.assertEqual(sale.price, self.product_1.price)

    def test_sale_price_for_product_2(self):
        order = Order.objects.create(user=self.user, shipping_option=self.shipping_1)
        order.products.add(self.product_2)
        sale = Sale.objects.create(product=self.product_2, order=order, quantity=43)
        order.save()
        self.assertEqual(sale.price, self.product_2.price)

    def test_order_total_price_after_changing_product_price(self):
        order = Order.objects.create(user=self.user, shipping_option=self.shipping_1)

        self.product_1 = Product.objects.create(name='Material 1', price=10.00)
        self.product_2 = Product.objects.create(name='Material 2', price=2.00)
        order.products.add(self.product_1, self.product_2)
        Sale.objects.create(product=self.product_1, order=order, quantity=3)
        Sale.objects.create(product=self.product_2, order=order, quantity=5)
        order.save()
        self.assertEqual(order.total_price, 47.00)

    def test_order_after_adding_extra_product(self):
        order = Order.objects.create(user=self.user, shipping_option=self.shipping_1)
        order.products.add(self.product_1, self.product_2)
        Sale.objects.create(product=self.product_1, order=order, quantity=2)
        Sale.objects.create(product=self.product_2, order=order, quantity=4)

        self.product_3 = Product.objects.create(name='Material 3', price=0.00)
        order.products.add(self.product_3)
        Sale.objects.create(product=self.product_3, order=order, quantity=2)

        order.save()
        self.assertEqual(order.products.all().count(), 3)



if __name__ == "__main__":
    unittest.main()
