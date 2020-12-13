import random
from django.shortcuts import render
from .apps import PagesConfig


theme = PagesConfig.theme

# Create your views here.
def home_view(request, *args, **kwargs):
	template_name = theme + '/index.html'
	webpage_name = "Home"
	context = {
		"webpage_name": webpage_name,
	}
	return render(request, template_name, context)

def about_view(request, *args, **kwargs):
	template_name = theme + '/about.html'
	webpage_name = "About"
	context = {
		"webpage_name": webpage_name,
	}
	return render(request, template_name, context)

def contact_view(request, *args, **kwargs):
	template_name = theme + '/contact.html'
	webpage_name = "Contact"
	context = {
		"webpage_name": webpage_name,
	}
	return render(request, template_name, context)

def dev_view(request, *args, **kwargs):

	def getSm():
		random.choice([2,2,2,2,3,3,4])

	template_name = theme + '/dev.html'
	webpage_name = "Dev"
	context = {
		"webpage_name": webpage_name,
		"list": range(10),
		"sm": getSm()
	}
	return render(request, template_name, context)
