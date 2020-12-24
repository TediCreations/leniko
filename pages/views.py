import random
from django.shortcuts import render

from .apps import PagesConfig

from products.models import Product

theme = PagesConfig.theme


def handler404(request, *args, **argv):
	template_name = theme + '/error.html'
	webpage_name = "404"
	webpage_description = "404 error"

	context = {
		"webpage_name":        webpage_name,
		"webpage_description": webpage_description,
		"previousUrl":         request.META.get('HTTP_REFERER'),
		"Message":             "The page you requested cannot be found!",
	}

	request.status_code = 404
	return render(request, template_name, context)


def handler500(request, *args, **argv):
	template_name = theme + '/error.html'
	webpage_name = "500"
	webpage_description = "500 error"

	context = {
		"webpage_name":        webpage_name,
		"webpage_description": webpage_description,
		"previousUrl":         request.META.get('HTTP_REFERER'),
		"Message":             "Server error! We are informed!",
	}

	request.status_code = 500
	return render(request, template_name, context)


def home_view(request, *args, **kwargs):
	template_name = theme + '/home.html'
	webpage_name = "Home"
	webpage_description = "Leniko jewelry home page"

	objList = Product.objects.filter(isActive = True)

	context = {
		"webpage_name":        webpage_name,
		"webpage_description": webpage_description,
		"objList":             objList
	}
	return render(request, template_name, context)


def about_view(request, *args, **kwargs):
	template_name = theme + '/about.html'
	webpage_name = "About"
	webpage_description = "Leniko jewelry about page"
	context = {
		"webpage_name":        webpage_name,
		"webpage_description": webpage_description,
	}
	return render(request, template_name, context)


def contact_view(request, *args, **kwargs):
	template_name = theme + '/contact.html'
	webpage_name = "Contact"
	webpage_description = "Leniko jewelry contact page"
	context = {
		"webpage_name":        webpage_name,
		"webpage_description": webpage_description,
	}
	return render(request, template_name, context)


def dev_view(request, *args, **kwargs):
	template_name = theme + '/dev.html'
	webpage_name = "Test"
	webpage_description = "Leniko jewelry test page"

	objList = Product.objects.all()

	context = {
		"webpage_name":        webpage_name,
		"webpage_description": webpage_description,
		"objList":             objList
	}
	return render(request, template_name, context)

def dev_form(request, *args, **kwargs):
	template_name = theme + '/dev/form.html'
	webpage_name = "Test"
	webpage_description = "Leniko jewelry test page"

	context = {
		"webpage_name":        webpage_name,
		"webpage_description": webpage_description,
	}
	return render(request, template_name, context)
