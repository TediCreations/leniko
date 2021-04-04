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

from .forms import BillingForm
from .forms import ShippingForm

from pages.apps import PagesConfig


theme = PagesConfig.theme

CHECKOUTSTEP_SESSION_ID = "checkoutStep"
BILLINGFORM_SESSION_ID = "billingForm"
SHIPPINGFORM_SESSION_ID = "shippingForm"
CHECKOUTINFO_SESSION_ID = "checkoutInfo"


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
				self.request.session[BILLINGFORM_SESSION_ID] = form.cleaned_data
				self.request.session.modified = True

				# Get cleaned data fromthe form
				billing = dict()
				billing['billing_firstName'] = form.cleaned_data['billing_firstName']
				billing['billing_lastName'] = form.cleaned_data['billing_lastName']
				billing['billing_phone'] = form.cleaned_data['billing_phone']
				billing['billing_email'] = form.cleaned_data['billing_email']
				billing['billing_address'] = form.cleaned_data['billing_address']
				billing['billing_address2'] = form.cleaned_data['billing_address2']
				billing['billing_town'] = form.cleaned_data['billing_town']
				billing['billing_state'] = form.cleaned_data['billing_state']
				billing['billing_country'] = form.cleaned_data['billing_country']
				billing['billing_postalCode'] = form.cleaned_data['billing_postalCode']

				billing['isShippingAddress'] = form.cleaned_data['isShippingAddress']
				billing['paymentOption'] = form.cleaned_data['paymentOption']

				if billing['isShippingAddress'] is True:

					# Create shipping form
					shipping = dict()
					shipping['shipping_firstName'] = billing['billing_firstName']
					shipping['shipping_lastName'] = billing['billing_lastName']
					shipping['shipping_phone'] = billing['billing_phone']
					shipping['shipping_email'] = billing['billing_email']
					shipping['shipping_address'] = billing['billing_address']
					shipping['shipping_address2'] = billing['billing_address2']
					shipping['shipping_town'] = billing['billing_town']
					shipping['shipping_state'] = billing['billing_state']
					shipping['shipping_country'] = billing['billing_country']
					shipping['shipping_postalCode'] = billing['billing_postalCode']

					shippingForm = ShippingForm(shipping)
					if shippingForm.is_valid():
						# Save form
						self.request.session[SHIPPINGFORM_SESSION_ID] = shippingForm.cleaned_data
						self.request.session.modified = True

						#
						order = {**billing, **shipping}
						self.request.session[CHECKOUTINFO_SESSION_ID] = order
						self.request.session.modified = True

						# We can skip shipping page
						self._writeSession(CheckOutEnum.CONFIRM)
					else:
						# Critical error
						print("\033[91mCRITICAL ERROR!!!!\033[0m")
						print(f"Errors: {shippingForm.errors}")
				else:
					# We can not skip the shiping page
					self._writeSession(CheckOutEnum.SHIPPING)
			else:
				print(f"\033[91mERROR in FORM\033[0m | {form.errors}")
		elif self.state == CheckOutEnum.SHIPPING:
			pass
		elif self.state == CheckOutEnum.CONFIRM:

			# ------------------------------------------------------
			# Cart
			cart = Cart.objects.find(self.request)

			# ------------------------------------------------------
			# Time
			today = date.today()

			def date_by_adding_business_days(from_date, add_days):
				business_days_to_add = add_days
				current_date = from_date
				while business_days_to_add > 0:
					current_date += timedelta(days=1)
					weekday = current_date.weekday()
					if weekday >= 5:  # sunday = 6
						continue
					business_days_to_add -= 1
				return current_date

			estimatedDeliveryDate = date_by_adding_business_days(today, config.ORDER_DELIVERY_DAYS)

			# ------------------------------------------------------
			# Products
			products = list()
			for cart_item in cart:
				product = dict()
				product["name"] = cart_item.product.getTitle()
				product["quantity"] = cart_item.quantity
				product["total"] = cart_item.total_price()
				product["url"] = cart_item.product.get_absolute_url()
				products.append(product)

			# ------------------------------------------------------
			# Order
			order = dict()
			order["ref_code"] = "63473458356934568"
			order["created_at"] = today

			order["name"] = "Elias"
			order["surname"] = "Kaneliss"
			order["billing_email"] = "hkanelhs@yahoo.gr"

			order["shipping_address"] = "Konstanta 22"
			order["shipping_address2"] = None
			order["shipping_city"] = "Volos"
			order["shipping_country"] = "Greece"
			order["shipping_postalCode"] = "38333"
			order["shipping_email"] = "support@leniko.gr"
			# order["phone"] = "6981957165"

			order["estimatedDeliveryDate"] = estimatedDeliveryDate
			order["products"] = products
			order["total"] = cart.get_total_price()

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

			emails = set([order["billing_email"], order["shipping_email"]])

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
