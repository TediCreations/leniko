from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from django_countries import countries

from cart.models import Cart
from .models import CheckOutEnum

from .forms import BillingForm
from .forms import ShippingForm

from pages.apps import PagesConfig


theme = PagesConfig.theme

CHECKOUTSTEP_SESSION_ID = "checkoutStep"
BILLINGFORM_SESSION_ID = "billingForm"
SHIPPINGFORM_SESSION_ID = "shippingForm"


class CheckOutManager(object):

	def __init__(self, request):
		self.request = request
		self.state = self._readSession()

	def _readSession(self):
		state = self.request.session.get(CHECKOUTSTEP_SESSION_ID)
		return CheckOutEnum.str2Enum(state)

	def _writeSession(self, state):
		self.request.session[CHECKOUTSTEP_SESSION_ID] = state.value
		self.request.session.modified = True

	def getState(self):
		return self.state

	def setState(self, state):
		self.state = state

	def handle(self):
		print(f"State = \033[92m{self.state.value}\033[0m")

		if self.state == CheckOutEnum.N:
			self._writeSession(CheckOutEnum.BILLING)
		elif self.state == CheckOutEnum.BILLING:
			form = BillingForm(self.request.POST)
			if form.is_valid():
				# Save form
				self.request.session['BILLINGFORM_SESSION_ID'] = form.cleaned_data
				self.request.session.modified = True

				# Get cleaned data fromthe form
				billing = dict()
				billing['firstName'] = form.cleaned_data['billing_firstName']
				billing['lastName'] = form.cleaned_data['billing_lastName']
				billing['phone'] = form.cleaned_data['billing_phone']
				billing['email'] = form.cleaned_data['billing_email']
				billing['address'] = form.cleaned_data['billing_address']
				billing['address2'] = form.cleaned_data['billing_address2']
				billing['town'] = form.cleaned_data['billing_town']
				billing['state'] = form.cleaned_data['billing_state']
				billing['country'] = form.cleaned_data['billing_country']
				billing['postalCode'] = form.cleaned_data['billing_postalCode']

				billing['isShippingAddress'] = form.cleaned_data['isShippingAddress']
				billing['paymentOption'] = form.cleaned_data['paymentOption']

				if billing['isShippingAddress'] is True:

					# Create shipping form
					shipping = dict()
					shipping['shipping_firstName'] = billing['firstName']
					shipping['shipping_lastName'] = billing['lastName']
					shipping['shipping_phone'] = billing['phone']
					shipping['shipping_email'] = billing['email']
					shipping['shipping_address'] = billing['address']
					shipping['shipping_address2'] = billing['address2']
					shipping['shipping_town'] = billing['town']
					shipping['shipping_state'] = billing['state']
					shipping['shipping_country'] = billing['country']
					shipping['shipping_postalCode'] = billing['postalCode']

					shippingForm = ShippingForm(initial=shipping)
					if shippingForm.is_valid():
						# Save form
						self.request.session['SHIPPING_SESSION_ID'] = shippingForm.cleaned_data
						self.request.session.modified = True

						# We can skip shipping page
						self._writeSession(CheckOutEnum.CONFIRM)
					else:
						# Critical error
						print("\033[91mERROR ERROR ERROR ERROR ERROR ERROR ERROR !!!!!!!!!!!!!!!!!!!!\033[0m")
						# print(f"Form:   {shippingForm}")
						print(f"Errors: {shippingForm.errors}")
						print(f"Errors: {shippingForm.non_field_errors()}")
				else:
					# We can not skip the shiping page
					self._writeSession(CheckOutEnum.SHIPPING)

				# Debug
				for key in billing:
					print(f"B: {key} = {billing[key]}")
				#for key in shipping:
				#	print(f"S: {key} = {shipping[key]}")

			else:
				print(f"\033[91mERROR in FORM\033[0m | {form.errors}")
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

		manager = CheckOutManager(request)

		# manager.debug("GET PRE")
		checkoutState = manager.getState()
		# manager.debug("GET POST")

		# Decide view
		if checkoutState == CheckOutEnum.N:
			return HttpResponseRedirect(reverse("cart:detail"))
		if checkoutState == CheckOutEnum.BILLING:
			template_name = theme + '/checkout/billing.html'
			form = BillingForm(initial=self.request.session.get('BILLINGFORM_SESSION_ID'))
		elif checkoutState == CheckOutEnum.SHIPPING:
			template_name = theme + '/checkout/shipping.html'
			form = ShippingForm(initial=self.request.session.get('SHIPPINGFORM_SESSION_ID'))
		elif checkoutState == CheckOutEnum.CONFIRM:
			template_name = theme + '/checkout/confirm.html'
			form = None  # ConfirmForm(initial=self.request.session.get('confirmForm'))
		elif checkoutState == CheckOutEnum.SUCCESS:
			return HttpResponseRedirect(reverse("products:list"))
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
			"form": form
		}

		return render(request, template_name, context)

	def post(self, request):

		manager = CheckOutManager(request)
		manager.debug("POST PRE")
		manager.handle()
		# manager.debug("POST POST")
		return HttpResponseRedirect(reverse("checkout:checkout"))
