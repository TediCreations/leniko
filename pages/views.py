import random
from django.shortcuts import render
from .apps import PagesConfig

from products.models import Product

theme = PagesConfig.theme

# Create your views here.
def home_view(request, *args, **kwargs):
	template_name = theme + '/home.html'
	webpage_name = "Home"
	webpage_description = "Leniko jewelry home page"
	context = {
		"webpage_name":        webpage_name,
		"webpage_description": webpage_description,
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
	template_name = theme + '/shopbase.html'
	webpage_name = "Test"
	webpage_description = "Leniko jewelry test page"

	#objList = None
	objList = Product.objects.all()
	#objList = Product.objects.filter(isActive = True)

	context = {
		"webpage_name":        webpage_name,
		"webpage_description": webpage_description,
		"objList":             objList
	}
	return render(request, template_name, context)
