from django.core.management.base import BaseCommand
from cart.models import Cart
from cart.models import CartItem
from products.models import Product

import random


class Command(BaseCommand):

	help = 'Work with carts'

	def add_arguments(self, parser):
		parser.add_argument('-l', '--list', action='store_true', help='List carts')
		parser.add_argument('-i', '--delete_item', type=int, help='Delete item given the id')
		parser.add_argument('-c', '--delete_cart', type=int, help='Delete cart given the id')
		parser.add_argument('-m', '--mock', action='store_true', help='Populate with mock data')
		parser.add_argument('-d', '--delete', action='store_true', help='Delete all carts')

	def handle(self, *args, **options):

		delete_item_number = options['delete_item']
		delete_cart_number = options['delete_cart']

		if options['list'] is True:
			self._list()

		elif options['delete'] is True:
			self._delete()

		elif options['mock'] is True:
			cartNum = random.randint(1, 10)
			for c in range(cartNum):
				cart = Cart()
				cart.save()
				print(f"Created \033[91m{cart}\033[0m")
				itemNum = random.randint(0, 10)
				for i in range(itemNum):
					product = random.choice(Product.objects.all())
					quantity = random.randint(1, 10)
					price = product.price
					cart = cart

					item = CartItem(
						product=product,
						quantity=quantity,
						price=price,
						cart=cart)
					item.save()
					print(f"\tCreated \033[92m{item}\033[0m")

		elif delete_item_number:
			self._delete_cartItem(delete_item_number)

		elif delete_cart_number:
			self._delete_cart(delete_cart_number)

	def _list(self):
		carts = Cart.objects.all()
		for cart in carts:
			print("---------------------------------------------")
			print(f"Cart: \033[91m{cart}\033[0m with id=\033[91m{cart.id}\033[0m")
			for item in cart:
				print(f"\tItem: \033[92m{item.quantity}\033[0m x \033[92m{item}\033[0m with id=\033[92m{item.id}\033[0m")
			print()
		cartLen = len(carts)
		itemLen = len(CartItem.objects.all())
		self.stdout.write(self.style.SUCCESS(f"Found {cartLen} carts with {itemLen} items"))

	def _delete(self):
		carts = Cart.objects.all()
		for cart in carts:
			cart.delete()
			self.stdout.write(self.style.SUCCESS(f"Deleted cart: \033[92m{cart}\033[0m"))

	def _mock(self):
		cartNum = random.randint(1, 10)
		for c in range(cartNum):
			cart = Cart()
			cart.save()
			print(f"Created \033[91m{cart}\033[0m")
			itemNum = random.randint(0, 10)
			for i in range(itemNum):
				product = random.choice(Product.objects.all())
				quantity = random.randint(1, 10)
				price = product.price
				cart = cart

				item = CartItem(
					product=product,
					quantity=quantity,
					price=price,
					cart=cart)
				item.save()
				print(f"\tCreated \033[92m{item}\033[0m")

	def _delete_cartItem(self, cartItem_id):
		try:
			item = CartItem.objects.get(id=cartItem_id)
		except Exception:
			self.stdout.write(self.style.ERROR(f"Item with id={cartItem_id} is not available"))
		else:
			item.delete()
			self.stdout.write(self.style.SUCCESS(f"Deleted item: \033[92m{item}\033[0m"))

	def _delete_cart(self, cart_id):
		try:
			cart = Cart.objects.get(id=cart_id)
		except Exception:
			self.stdout.write(self.style.ERROR(f"Cart with id={cart_id} is not available"))
		else:
			cart.delete()
			self.stdout.write(self.style.SUCCESS(f"Deleted cart: \033[92m{cart}\033[0m"))
