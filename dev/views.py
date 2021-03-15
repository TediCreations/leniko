from django.shortcuts import render

from products.models import Product
from cart.models import Cart
from pages.apps import PagesConfig

theme = PagesConfig.theme


def dev_view(request, *args, **kwargs):
	template_name = theme + '/dev.html'
	webpage_name = "Test"
	webpage_description = "Leniko jewelry test page"

	# --------------------------------------------------
	# Cart
	cart = Cart(request)

	# --------------------------------------------------
	# Products
	objList = Product.objects.all()

	context = {
		"webpage_name": webpage_name,
		"webpage_description": webpage_description,
		"objList": objList,
		"cart": cart
	}
	return render(request, template_name, context)


def dev_form(request, *args, **kwargs):
	template_name = theme + '/dev/form.html'
	webpage_name = "Test"
	webpage_description = "Leniko jewelry test page"

	# --------------------------------------------------
	# Cart
	cart = Cart(request)

	context = {
		"webpage_name": webpage_name,
		"webpage_description": webpage_description,
		"cart": cart
	}
	return render(request, template_name, context)


def dev_coming_soon(request, *args, **kwargs):
	template_name = theme + '/coming-soon.html'
	webpage_name = "Coming soon"
	webpage_description = "Coming soon!!!"

	context = {
		"webpage_name": webpage_name,
		"webpage_description": webpage_description
	}
	return render(request, template_name, context)
