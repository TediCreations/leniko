import random

from django.http         import HttpResponseRedirect
from django.shortcuts    import render
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.views        import View


from products.models import Product

from .apps import PagesConfig

theme = PagesConfig.theme


def handler400(request, *args, **argv):
	template_name = theme + '/error.html'
	webpage_name = "400"
	webpage_description = "400 error"

	context = {
		"webpage_name":        webpage_name,
		"webpage_description": webpage_description,
		"previousUrl":         request.META.get('HTTP_REFERER'),
		"Message":             "Bad request!",
	}

	request.status_code = 400
	return render(request, template_name, context)


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


def login_view(request, *args, **kwargs):

	# Default place to redirect after login is the home page
	login_msg = "Great to have you back!"

	# Default place to redirect after login is the home page
	next_url = "/"
	# Get the url to redirect to if it exists
	try:
		next_url = request.GET['next']
	except Exception:
		pass

	# With POST we attempt to login
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			# Authenticated
			login(request, user)
			return HttpResponseRedirect(next_url)
		else:
			#Did not authenticate
			return HttpResponseRedirect(f'?next={next_url}')

	else:

		if request.user.is_authenticated:
			# No need to see login page
			return HttpResponseRedirect(next_url)
		else:
			template_name = theme + '/login-register.html'
			webpage_name = "Login or Register"
			webpage_description = "Leniko jewelry login or register page"

			context = {
				"webpage_name":        webpage_name,
				"webpage_description": webpage_description,
				"login_msg":           login_msg
			}
			return render(request, template_name, context)


def logout_view(request, *args, **kwargs):
	# Default place to redirect after login is the home page
	next_url = "/"

	# Get the url to redirect to if it exists
	try:
		next_url = request.GET['next']
	except Exception:
		pass

	logout(request)
	return HttpResponseRedirect(next_url)


class HomeView(View):

	"""Show the website's home page"""

	template_name = theme + '/home.html'
	webpage_name = "Home"
	webpage_description = "Leniko jewelry home page"

	def get(self, request):

		objList = Product.objects.filter(isActive=True).filter(isFeatured=True)[:10]

		context = {
			"webpage_name": self.webpage_name,
			"webpage_description": self.webpage_description,
			"objList": objList
		}
		return render(request, self.template_name, context)


class AboutView(View):

	"""Show the website's about page"""

	template_name = theme + '/about.html'
	webpage_name = "About"
	webpage_description = "Leniko jewelry about page"

	def get(self, request):

		context = {
			"webpage_name": self.webpage_name,
			"webpage_description": self.webpage_description,
		}
		return render(request, self.template_name, context)


class ContactView(View):

	"""Show the website's contact page"""

	template_name = theme + '/contact.html'
	webpage_name = "Contact"
	webpage_description = "Leniko jewelry contact page"

	def get(self, request):

		context = {
			"webpage_name": self.webpage_name,
			"webpage_description": self.webpage_description,
		}
		return render(request, self.template_name, context)


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

def dev_coming_soon(request, *args, **kwargs):
	template_name = theme + '/coming-soon.html'
	webpage_name = "Coming soon"
	webpage_description = "Coming soon!!!"

	objList = Product.objects.all()

	context = {
		"webpage_name":        webpage_name,
		"webpage_description": webpage_description
	}
	return render(request, template_name, context)
