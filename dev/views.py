from django.shortcuts import render
from django.views import View

from products.models import Product
from cart.models import Cart
from pages.apps import PagesConfig

theme = PagesConfig.theme


class DevView(View):

	template_name = theme + '/dev.html'
	webpage_name = "Dev"
	webpage_description = "Leniko jewelry test page"

	def get(self, request):

		# --------------------------------------------------
		# Cart
		cart = Cart(request)

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
		cart = Cart(request)

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
		cart = Cart(request)

		context = {
			"webpage_name": self.webpage_name,
			"webpage_description": self.webpage_description,
			"cart": cart
		}
		return render(request, self.template_name, context)
