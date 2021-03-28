from django.db import models

from django_countries.fields import CountryField

import uuid


"""
https://testdriven.io/blog/django-custom-user-model/
class Customer(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	surname = models.CharField(max_length=50, blank=True, null=True)
	surname = models.CharField(max_length=50, blank=True, null=True)
	billingAddress = models.CharField(max_length=50, blank=True, null=True)
	shippingAddress = models.CharField(max_length=50, blank=True, null=True)
"""


class Order(models.Model):

	ref_code = models.CharField(max_length=50, blank=True, null=True, editable=False)
	dateCreated = models.DateTimeField(auto_now_add=True, editable=False)
	isPayed = models.BooleanField(default=False)
	isDispatched = models.BooleanField(default=False)
	isRefundAsked = models.BooleanField(default=False)
	isRefunded = models.BooleanField(default=False)

	billing_address = models.CharField(max_length=100, blank=True, null=True)
	billing_address2 = models.CharField(max_length=100, blank=True, null=True)
	billing_country = CountryField()
	billing_zip = models.CharField(max_length=5, blank=True, null=True)

	shipping_address = models.CharField(max_length=100, blank=True, null=True)
	shipping_address2 = models.CharField(max_length=100, blank=True, null=True)
	shipping_country = CountryField()
	shipping_zip = models.CharField(max_length=5, blank=True, null=True)

	def __str__(self):
		return self.ref_code

	def save(self, *args, **kwargs):
		if not self.ref_code:
			self.ref_code = str(uuid.uuid4().hex)

		super().save(*args, **kwargs)


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	sku = models.TextField(default=None, blank=False, null=False, editable=False)
	quantity = models.IntegerField(blank=False, null=False, editable=False)
	unit_price = models.FloatField(blank=False, null=False, editable=False)

	def __str__(self):
		return f"{self.quantity} x {self.sku}"
