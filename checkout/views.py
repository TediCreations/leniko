from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from django_countries import countries

from cart.models import Cart
from checkout.models import CheckOutEnum
from pages.apps import PagesConfig


theme = PagesConfig.theme

CHECKOUTSTEP_SESSION_ID = "checkoutStep"


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
		self._writeSession(CheckOutEnum.BILLING)

		# if self.state == CheckOutEnum.BILLING:
		# 	self._writeSession(CheckOutEnum.CONFIRM)
		# else:
		# 	self._writeSession(CheckOutEnum.BILLING)

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
			print(f'{key}: {value}')
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

		manager.debug("GET PRE")
		checkoutState = manager.getState()
		manager.debug("GET POST")

		# Decide view
		if checkoutState == CheckOutEnum.N:
			return HttpResponseRedirect(reverse("cart:detail"))
		if checkoutState == CheckOutEnum.BILLING:
			template_name = theme + '/checkout/billing.html'
		elif checkoutState == CheckOutEnum.SHIPPING:
			template_name = theme + '/checkout/shipping.html'
		elif checkoutState == CheckOutEnum.CONFIRM:
			template_name = theme + '/checkout/confirm.html'
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
			"countries": countries
		}

		return render(request, template_name, context)

	def post(self, request):

		manager = CheckOutManager(request)
		manager.debug("POST PRE")
		manager.handle()
		manager.debug("POST POST")
		return HttpResponseRedirect(reverse("checkout:checkout"))
