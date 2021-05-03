from django.db import models

from django_countries.fields import CountryField

from enum import Enum
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


class CheckOutEnum(Enum):
	N = "None"
	BILLING = "Billing"
	SHIPPING = "Shipping"
	OVERVIEW = "Overview"
	PAYMENT = "Payment"
	SUCCESS = "Success"
	FAIL = "Fail"
	# CONFIRM = "Confirm"

	@staticmethod
	def str2Enum(s):
		for e in CheckOutEnum:
			if s == e.value:
				return e
		return CheckOutEnum.N


# def getUniqueId():
# 	return str(uuid.uuid4().hex)


class Order(models.Model):

	# System
	# ref_code = models.UUIDField(primary_key=True, default=getUniqueId, editable=False)
	ref_code = models.CharField(max_length=32, blank=True, null=True, editable=False)
	created_at = models.DateTimeField(auto_now_add=True, editable=False)

	# Stripe
	stripe_id = models.CharField(max_length=50, blank=True, null=True, editable=False)

	# Status
	isPayed = models.BooleanField(default=False)
	isDispatched = models.BooleanField(default=False)
	isRefundAsked = models.BooleanField(default=False)
	isRefunded = models.BooleanField(default=False)

	# Billing details
	billing_firstName = models.CharField(max_length=50, blank=True, null=True)
	billing_lastName = models.CharField(max_length=100, blank=True, null=True)
	billing_email = models.EmailField(max_length=254, blank=True, null=True)
	billing_address = models.CharField(max_length=100, blank=True, null=True)
	billing_address2 = models.CharField(max_length=100, blank=True, null=True)
	billing_city = models.CharField(max_length=100, blank=True, null=True)
	billing_country = CountryField()
	billing_postalCode = models.CharField(max_length=5, blank=True, null=True)

	# Shipping details
	shipping_firstName = models.CharField(max_length=50, blank=True, null=True)
	shipping_lastName = models.CharField(max_length=100, blank=True, null=True)
	shipping_email = models.EmailField(max_length=254, blank=True, null=True)
	shipping_address = models.CharField(max_length=100, blank=True, null=True)
	shipping_address2 = models.CharField(max_length=100, blank=True, null=True)
	shipping_city = models.CharField(max_length=100, blank=True, null=True)
	shipping_country = CountryField()
	shipping_postalCode = models.CharField(max_length=5, blank=True, null=True)

	estimatedDeliveryDate = models.DateTimeField(blank=True, null=True)
	total = models.FloatField(blank=False, null=False)

	def __str__(self):
		return self.ref_code

	def save(self, *args, **kwargs):
		if not self.ref_code:
			self.ref_code = str(uuid.uuid4().hex)

		super().save(*args, **kwargs)


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	sku = models.TextField(default=None, blank=False, null=False, editable=False)
	name = models.TextField(default=None, blank=False, null=False, editable=False)
	quantity = models.IntegerField(blank=False, null=False, editable=False)
	unit_price = models.FloatField(blank=False, null=False, editable=False)

	def __str__(self):
		return f"{self.quantity} x {self.sku}"
