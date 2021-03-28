from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from products.models import Product
from cart.models import Cart
from pages.apps import PagesConfig
from django.conf import settings

import stripe

theme = PagesConfig.theme


class DevView(View):

	template_name = theme + '/dev.html'
	webpage_name = "Dev"
	webpage_description = "Leniko jewelry test page"

	def get(self, request):

		# --------------------------------------------------
		# Cart
		cart = Cart.objects.find(request)

		# --------------------------------------------------
		# Products
		objList = Product.objects.all()

		context = {
			"webpage_name": self.webpage_name,
			"webpage_description": self.webpage_description,
			"objList": objList,
			"cart": cart
		}
		return render(request, self.template_name, context)


class TestView(View):

	template_name = theme + '/dev/test.html'
	webpage_name = "Form"
	webpage_description = "Form!"

	def get(self, request):

		# --------------------------------------------------
		# Cart
		cart = Cart.objects.find(request)

		context = {
			"webpage_name": self.webpage_name,
			"webpage_description": self.webpage_description,
			"cart": cart
		}
		return render(request, self.template_name, context)


class CommingSoonView(View):

	template_name = theme + '/coming-soon.html'
	webpage_name = "Coming soon"
	webpage_description = "Coming soon!!!"

	def get(self, request):

		context = {
			"webpage_name": self.webpage_name,
			"webpage_description": self.webpage_description
		}
		return render(request, self.template_name, context)


class PayView(View):

	template_name = theme + '/dev/pay.html'
	webpage_name = "Pay"
	webpage_description = "Leniko jewelry test pay page"

	def get(self, request):

		# --------------------------------------------------
		# Cart
		cart = Cart.objects.find(request)

		stripe_public_key = settings.STRIPE_PUBLIC_KEY

		context = {
			"webpage_name": self.webpage_name,
			"webpage_description": self.webpage_description,
			"cart": cart,
			"stripe_public_key": stripe_public_key
		}
		return render(request, self.template_name, context)

	def post(self, request):
		"""Create Stripe payment intent"""

		# --------------------------------------------------
		# Cart
		cart = Cart.objects.find(request)
		total = int(cart.get_total_price() * 100)  # We multiply with 100 because Stripe uses cents

		stripe.api_key = settings.STRIPE_SECRET_KEY

		try:
			intent = stripe.PaymentIntent.create(
				amount=total,
				currency='eur'
			)

			print(f"Intent: {intent}")

			return JsonResponse({
				'clientSecret': intent['client_secret']
			})
		except Exception as e:
			return JsonResponse({"error": str(e)}, status=403)
