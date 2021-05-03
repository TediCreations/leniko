from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# from .forms import CartAddProductForm

from products.models import Product


CART_SESSION_ID = "cart"


class CartManager(models.Manager):

	def get_queryset(self):
		return super().get_queryset()

	def find(self, request):
		"""
		Retrieve the cart. Create if none.
		"""

		# return Cart(request)
		# if user.exists:
		# 	cart = MyCart.objects.get()
		# else:
		# 	cart =

		session = request.session
		cart_id = session.get(CART_SESSION_ID)
		if not cart_id:
			# save an empty cart in the session
			cart = Cart()
			cart.save()
			cart_id = session[CART_SESSION_ID] = cart.id
			session.modified = True

		cart = None
		try:
			cart = Cart.objects.get(id=cart_id)
		except Cart.DoesNotExist:
			# We have a session but cart was deleted from db
			cart = Cart()
			cart.save()
			cart_id = session[CART_SESSION_ID] = cart.id
			session.modified = True
		finally:
			return cart


class Cart(models.Model):

	"""Database based Cart"""

	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now_add=True)

	objects = CartManager()

	def add(self, product, quantity=1, update_quantity=False):
		"""
		Add an item to the cart or update its quantity.
		"""

		# Get items on this cart
		# print(f"Self: {self}")
		# cartItems = CartItem.objects.filter(cart=self)
		# print(f"cartItems: {cartItems}")

		# Get cartItem if previously was added
		cartItem = None
		try:
			cartItem = CartItem.objects.filter(cart=self).get(product=product)
		except CartItem.DoesNotExist:
			# Create a new cart item
			cartItem = CartItem(
				product=product,
				quantity=0,
				price=product.price,
				cart=self
			)
		finally:
			# Update with the latest price
			cartItem.price = product.price

			if update_quantity:
				cartItem.quantity = quantity
			else:
				cartItem.quantity += quantity
			now = timezone.now()
			self.modified_at = now
			cartItem.save()

	def remove(self, product):
		"""
		Remove an item from the cart.
		"""
		try:
			cartItem = CartItem.objects.filter(cart=self).get(product=product)
		except CartItem.DoesNotExist:
			pass
		else:
			now = timezone.now()
			self.modified_at = now
			cartItem.delete()

	def __len__(self):
		"""
		Count all items in the cart.
		"""
		length = 0
		cartItems = CartItem.objects.filter(cart=self)
		for cartItem in cartItems:
			length += cartItem.quantity
		return length

	def __str__(self):
		return f"{self.created_at}"

	def __iter__(self):
		cartItems = CartItem.objects.filter(cart=self)
		for cartItem in cartItems:
			yield cartItem

	def get_total_price(self):
		total = 0

		cartItems = CartItem.objects.filter(cart=self)
		for cartItem in cartItems:
			total += cartItem.quantity * cartItem.price

		return total

	def clear(self):
		cartItems = CartItem.objects.filter(cart=self)
		for cartItem in cartItems:
			cartItem.delete()
		now = timezone.now()

		# Reset the creation datetime
		now = timezone.now()
		self.modified_at = now
		self.created_at = now

	def isEmpty(self):
		if self.__len__() == 0:
			return True
		else:
			return False


class CartItem(models.Model):

	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	price = models.DecimalField(blank=True, max_digits=10, decimal_places=2)
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

	def __str__(self):
		title = self.product.getTitle()
		return f"{title}"

	def total_price(self):
		return self.price * self.quantity

	def add_url(self):
		return reverse("cart:add", kwargs={'product_id': self.product.id})

	def remove_url(self):
		return reverse("cart:remove", kwargs={'product_id': self.product.id})
