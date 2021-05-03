from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.core.mail import EmailMessage
from django.template.loader import get_template

from django_countries import countries
from constance import config

from datetime import date
from datetime import timedelta

from cart.models import Cart
from .models import CheckOutEnum
from .models import Order
from .models import OrderItem

from .forms import BillingForm
from .forms import ShippingForm

from pages.apps import PagesConfig


theme = PagesConfig.theme

BILLINGFORM_SESSION_ID = "billingForm"
SHIPPINGFORM_SESSION_ID = "shippingForm"
CHECKOUTINFO_SESSION_ID = "checkoutInfo"


def date_by_adding_business_days(from_date, add_days):
	"""
	Add add_days business days to from_date
	"""
	business_days_to_add = add_days
	current_date = from_date
	while business_days_to_add > 0:
		current_date += timedelta(days=1)
		weekday = current_date.weekday()
		if weekday >= 5:  # sunday = 6
			continue
		business_days_to_add -= 1
	return current_date


class CheckOutManager(object):

	CHECKOUTSTEP_SESSION_ID = "checkoutStep"

	def __init__(self, request):
		self.request = request
		self.state = self._readSession()

	def _error(self, msg):
		print(f"[\033[91mERROR\033[0m] {msg}")

	def _readSession(self):
		state = self.request.session.get(self.CHECKOUTSTEP_SESSION_ID)
		return CheckOutEnum.str2Enum(state)

	def _writeSession(self, state):
		self.request.session[self.CHECKOUTSTEP_SESSION_ID] = state.value
		self.request.session.modified = True

	def getState(self):
		return self.state

	def setState(self, state):
		self.state = state

	def resetState(self):
		self.state = CheckOutEnum.N

	def handle(self):
		print(f"State = \033[92m{self.state.value}\033[0m")

		# Find cart
		cart = Cart.objects.find(self.request)
		if cart.isEmpty():
			self._writeSession(CheckOutEnum.N)
			return

		if self.state == CheckOutEnum.N:
			self._writeSession(CheckOutEnum.BILLING)
		elif self.state == CheckOutEnum.BILLING:
			form = BillingForm(self.request.POST)
			if form.is_valid():
				# Save form
				self.request.session[BILLINGFORM_SESSION_ID] = form.cleaned_data
				self.request.session.modified = True

				# Get cleaned data from the form
				billing = dict()
				for key in form.cleaned_data:
					billing[key] = form.cleaned_data[key]

				if billing['isShippingAddress'] is True:

					# Create shipping form
					shipping = dict()
					"""
					for key in billing:
						print(key)
						shipping[key] = billing[key]
					"""
					shipping['shipping_firstName'] = billing['billing_firstName']
					shipping['shipping_lastName'] = billing['billing_lastName']
					shipping['shipping_phone'] = billing['billing_phone']
					shipping['shipping_email'] = billing['billing_email']
					shipping['shipping_address'] = billing['billing_address']
					shipping['shipping_address2'] = billing['billing_address2']
					shipping['shipping_city'] = billing['billing_city']
					shipping['shipping_state'] = billing['billing_state']
					shipping['shipping_country'] = billing['billing_country']
					shipping['shipping_postalCode'] = billing['billing_postalCode']

					shippingForm = ShippingForm(shipping)
					if shippingForm.is_valid():
						# Save form
						self.request.session[SHIPPINGFORM_SESSION_ID] = shippingForm.cleaned_data
						self.request.session.modified = True

						# Create order
						order = {**billing, **shipping}
						self.request.session[CHECKOUTINFO_SESSION_ID] = order
						self.request.session.modified = True

						# We can skip shipping page
						self._writeSession(CheckOutEnum.CONFIRM)
					else:
						# Critical error
						# print("\033[91mCRITICAL ERROR!!!!\033[0m")
						self._error(f"ShippingForm Error: {shippingForm.errors}")
				else:
					# We can not skip the shipping page
					self._writeSession(CheckOutEnum.SHIPPING)
			else:
				self._error(form.errors)
		elif self.state == CheckOutEnum.SHIPPING:
			form = ShippingForm(self.request.POST)
			if form.is_valid():
				# Save form
				self.request.session[SHIPPINGFORM_SESSION_ID] = form.cleaned_data
				self.request.session.modified = True

				# Get cleaned data from the form
				shipping = dict()
				shipping['shipping_firstName'] = form.cleaned_data['shipping_firstName']
				shipping['shipping_lastName'] = form.cleaned_data['shipping_lastName']
				shipping['shipping_phone'] = form.cleaned_data['shipping_phone']
				shipping['shipping_email'] = form.cleaned_data['shipping_email']
				shipping['shipping_address'] = form.cleaned_data['shipping_address']
				shipping['shipping_address2'] = form.cleaned_data['shipping_address2']
				shipping['shipping_city'] = form.cleaned_data['shipping_city']
				shipping['shipping_state'] = form.cleaned_data['shipping_state']
				shipping['shipping_country'] = form.cleaned_data['shipping_country']
				shipping['shipping_postalCode'] = form.cleaned_data['shipping_postalCode']

				# Get billing info from previous step
				billing = self.request.session[BILLINGFORM_SESSION_ID]

				# Create order
				order = {**billing, **shipping}
				self.request.session[CHECKOUTINFO_SESSION_ID] = order
				self.request.session.modified = True

				# We can skip shipping page
				self._writeSession(CheckOutEnum.CONFIRM)

		elif self.state == CheckOutEnum.CONFIRM:

			# ------------------------------------------------------
			# Time
			today = date.today()
			estimatedDeliveryDate = date_by_adding_business_days(today, config.ORDER_DELIVERY_DAYS)

			# ------------------------------------------------------
			# Get user input data
			userInput = self.request.session[CHECKOUTINFO_SESSION_ID]

			# ------------------------------------------------------
			# Order
			order = Order(
				stripe_id="TEST STRIPE ID",

				# Status
				isPayed=False,
				isDispatched=False,
				isRefundAsked=False,
				isRefunded=False,

				# Billing details
				billing_firstName=userInput["billing_firstName"],
				billing_lastName=userInput["billing_lastName"],
				billing_email=userInput["billing_email"],
				billing_address=userInput["billing_address"],
				billing_address2=userInput["billing_address2"],
				billing_city=userInput["billing_city"],
				billing_country=userInput["billing_country"],
				billing_postalCode=userInput["billing_postalCode"],

				# Shipping details
				shipping_firstName=userInput["shipping_firstName"],
				shipping_lastName=userInput["shipping_lastName"],
				shipping_email=userInput["shipping_email"],
				shipping_address=userInput["shipping_address"],
				shipping_address2=userInput["shipping_address2"],
				shipping_city=userInput["shipping_city"],
				shipping_country=userInput["shipping_country"],
				shipping_postalCode=userInput["shipping_postalCode"],

				estimatedDeliveryDate=estimatedDeliveryDate,
				total=cart.get_total_price()
			)
			order.save()

			# ------------------------------------------------------
			# Products
			for cart_item in cart:
				orderItem = OrderItem(
					order=order,
					sku=cart_item.product.sku,
					name=cart_item.product.getTitle(),
					quantity=cart_item.quantity,
					unit_price=cart_item.total_price()
				)
				orderItem.save()

			cart.clear()
			print("Cart is cleared")

			# ------------------------------------------------------
			# Email
			template_name = theme + '/emails/orderConfirmation.html'
			context = {
				"message": "Your order is being handled with care.",
				"order": order,
				"config": config,
				"shipping_cost": 5,
				"tax": 24,
			}

			message = get_template(template_name).render(context)

			emails = set([order.billing_email, order.shipping_email])

			try:
				mail = EmailMessage(
					subject=f'[INVOICE] | No: {order["ref_code"]}',
					body=message,
					from_email=config.EMAIL,
					to=list(emails),
					headers={'Content-Type': 'text/plain'},
				)
				mail.content_subtype = "html"
				mail.send()
				print("Mail sent")
			except Exception as e:
				print(f"Error: {e}")

			# Success
			self._writeSession(CheckOutEnum.SUCCESS)
		else:
			print("\033[91mState not coded yet!!!!!!!!!!!\033[0m")

	def debug(self, text=None):
		print('----------------------------------')
		if text:
			print(text)
		print('GET')
		for key, value in self.request.GET.items():
			print(f'{key}: {value}')
		print("")

		print('SESSION')
		for key, value in self.request.session.items():
			print(f'{key}: {value} | type={type(key)}')
		print("")


class CheckoutView(View):

	"""Show the website's checkout page

	0. Cart (Money > 0)

	1. Billing address (is shipping the same?)
	2. Shipping Address
	3. Checkout
	4. Pay
	5. Thank you(Success note)
	6. Critical Error (We are informed)

	"""

	webpage_name = "Checkout"
	webpage_description = "Leniko jewelry checkout page"

	def get(self, request):

		order = None
		form = None

		manager = CheckOutManager(request)

		# manager.debug("GET PRE")
		checkoutState = manager.getState()
		# manager.debug("GET POST")

		# Decide view
		if checkoutState == CheckOutEnum.N:
			return HttpResponseRedirect(reverse("cart:detail"))
		if checkoutState == CheckOutEnum.BILLING:
			template_name = theme + '/checkout/billing.html'
			form = BillingForm(initial=self.request.session.get(BILLINGFORM_SESSION_ID))
		elif checkoutState == CheckOutEnum.SHIPPING:
			template_name = theme + '/checkout/shipping.html'
			form = ShippingForm(initial=self.request.session.get(SHIPPINGFORM_SESSION_ID))
		elif checkoutState == CheckOutEnum.CONFIRM:
			template_name = theme + '/checkout/confirm.html'
			order = self.request.session.get(CHECKOUTINFO_SESSION_ID)
		elif checkoutState == CheckOutEnum.PAYMENT:
			template_name = theme + '/checkout/payment.html'
			order = self.request.session.get(CHECKOUTINFO_SESSION_ID)
		elif checkoutState == CheckOutEnum.SUCCESS:
			template_name = theme + '/checkout/success.html'
			order = self.request.session.get(CHECKOUTINFO_SESSION_ID)
		elif checkoutState == CheckOutEnum.FAIL:
			return HttpResponseRedirect(reverse("cart:detail"))
		else:
			return HttpResponseRedirect(reverse("cart:detail"))

		# --------------------------------------------------
		# Cart
		cart = Cart.objects.find(request)

		# --------------------------------------------------
		# Render
		context = {
			"webpage_name": self.webpage_name,
			"webpage_description": self.webpage_description,
			"cart": cart,
			"countries": countries,
			"form": form,
			"order": order
		}

		return render(request, template_name, context)

	def post(self, request):

		manager = CheckOutManager(request)
		# manager.debug("POST PRE")
		manager.handle()
		# manager.debug("POST POST")
		return HttpResponseRedirect(reverse("checkout:checkout"))
