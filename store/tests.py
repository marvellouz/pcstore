# -*- coding: utf-8 -*-

import unittest
from models import *

class CartTestCase(unittest.TestCase):
	def setUp(self):
		self.user=User.objects.create_user(username="a", email="a@mail.bg", password="a")
		self.cart=Cart.objects.create(customer=self.user)
		self.category=Category.objects.create(name="cat")
		self.product=Product.objects.create(name="prod", description="prod description", price=1, category=self.category)
		self.product_1=Product.objects.create(name="prod_1", description="prod_1 description", price=2, category=self.category)

	def tearDown(self):
		self.user.delete()
		self.cart.delete()
		self.category.delete()
		self.product.delete()
		self.product_1.delete()


	def test_add_item(self):
		self.cart.add_item(self.product, 1)
		self.cart.save()
		self.assertEqual(len(self.cart.cartitem_set.all()), 1)
		
		self.cart.add_item(self.product, 1)
		self.cart.save()
		self.assertEqual(len(self.cart.cartitem_set.all()), 1)

		self.cart.add_item(self.product_1, 1)
		self.cart.save()
		self.assertEqual(len(self.cart.cartitem_set.all()), 2)

	def test_remove_item(self):
		self.cart.add_item(self.product, 2)
		self.cart.save()
		self.cart.remove_item(self.cart.cartitem_set.all()[0])
		self.cart.save()
		
		self.assertEqual(len(self.cart.cartitem_set.all()), 0)

		self.assertRaises(ValueError, self.cart.remove_item, self.product)
	
	def test_isempty(self):

		self.assertTrue(self.cart.is_empty())

		self.cart.add_item(self.product, 1)
		self.cart.save()
		self.assertFalse(self.cart.is_empty())

	def test_total(self):
		self.assertEqual(self.cart.total(), 0)

		self.cart.add_item(self.product_1, 3)
		self.cart.save()

		self.assertEqual(self.product_1.price*3, self.cart.total())
		self.assertEqual(self.cart.cartitem_set.all()[0].price(), self.cart.total())
		self.assertEqual(self.cart.total(), 6)


class CartItemTestCase(unittest.TestCase):
	def setUp(self):
		self.user=User.objects.create_user(username="a", email="a@mail.bg", password="a")
		self.cart=Cart.objects.create(customer=self.user)
		self.category=Category.objects.create(name="cat")
		self.product=Product.objects.create(name="prod", description="prod description", price=1, category=self.category)
		self.cart_item=CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

	def tearDown(self):
		self.user.delete()
		self.cart.delete()
		self.category.delete()
		self.product.delete()
		self.cart_item.delete()

	def test_price(self):
		self.assertEqual(self.cart_item.price(), 2)
		
		self.cart_item.quantity=5
		self.assertEqual(self.cart_item.price(), 5)

class OrderItemTestCase(unittest.TestCase):
	def setUp(self):
		self.user=User.objects.create_user(username="a", email="a@mail.bg", password="a")
		self.cart=Cart.objects.create(customer=self.user)
		self.category=Category.objects.create(name="cat")
		self.product=Product.objects.create(name="prod", description="prod description", price=1, category=self.category)
		self.status=OrderStatus.objects.create(name="приета")
		self.courier=Courier.objects.create(name="speedy")
		self.pay_method=PayMethod.objects.create(name="epay")
		self.order=Order.objects.create(user=self.user, address="some address", status=self.status, courier=self.courier, pay_method=self.pay_method)
		self.order_item=OrderItem.objects.create(order=self.order, product=self.product, price=self.product.price, quantity=2)

	def tearDown(self):
		self.user.delete()
		self.cart.delete()
		self.category.delete()
		self.product.delete()
		self.order_item.delete()

	def test_item_price(self):
		self.product.price=2
		self.assertEquals(self.order_item.item_price(), 2)

