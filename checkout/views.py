from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from django_countries import countries

from cart.models import Cart
from pages.apps import PagesConfig


theme = PagesConfig.theme

CHECKOUTSTEP_SESSION_ID = "checkoutStep"


class CheckoutView(View):

	"""Show the website's checkout page

	0. Cart (Money > 0)

	1. Billing address (is shipping the same?)
	2. Shipping Address
	3. Checkout
	4. Pay
	5. Success note

	"""

	webpage_name = "Checkout"
	webpage_description = "Leniko jewelry checkout page"

	def _getCheckOutStep(self, request):

		# print('GET')
		# for key, value in request.GET.items():
		# 	print(f'{key}: {value}')

		# print('SESSION')
		# for key, value in request.session.items():
		# 	print(f'{key}: {value}')

		# page = request.GET.get('p')

		reachedCheckOutStep = request.session.get(CHECKOUTSTEP_SESSION_ID)

		if not reachedCheckOutStep:
			request.session[CHECKOUTSTEP_SESSION_ID] = "b"
			reachedCheckOutStep = "b"

		if reachedCheckOutStep == "b":
			request.session[CHECKOUTSTEP_SESSION_ID] = "s"
			template_name = theme + '/checkout/billing.html'
		elif reachedCheckOutStep == "s":
			request.session[CHECKOUTSTEP_SESSION_ID] = "c"
			template_name = theme + '/checkout/shipping.html'
		elif reachedCheckOutStep == "c":
			request.session[CHECKOUTSTEP_SESSION_ID] = "f"
			template_name = theme + '/checkout/confirm.html'
		else:
			template_name = None

		request.session.modified = True
		return template_name

	def get(self, request):

		# Get checkout step
		template_name = self._getCheckOutStep(request)
		if not template_name:
			return HttpResponseRedirect(reverse("products:list"))

		# --------------------------------------------------
		# Cart
		cart = Cart.objects.find(request)

		print("PRE CART")
		for i in cart:
			print(i)
		print("POST CART")

		print("PRE SESSION")
		print(request.session.items())
		print("POST SESSION")

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

		"""
		# --------------------------------------------------
		# Get checkout step
		request.session.modified = True
		self.session = request.session
		checkoutStep = self.session.get(CHECKOUTSTEP_SESSION_ID)
		if not checkoutStep:
			# save first
			checkoutStep = self.session[CHECKOUTSTEP_SESSION_ID] = {}
			checkoutStep["id"] = "1"
		else:
			checkoutStep["id"] = str(int(checkoutStep["id"]) + 1)
		step = checkoutStep["id"]
		step = str(step)

		print('POST')
		for key, value in request.POST.items():
			print(f'{key}: {value}')
		print(f'step: {step}')

		if step == "5":
			checkoutStep.clear()

		return HttpResponseRedirect(f"/checkout/?step={step}")
		"""

		return HttpResponseRedirect("/checkout")
