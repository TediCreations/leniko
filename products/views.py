from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .forms import ProductForm
from .models import Product

from pages.apps import PagesConfig


theme = PagesConfig.theme

def product_list_view(request):
	template_name = theme +'/shop.html'
	webpage_name = "Shop"
	webpage_description = "Leniko jewelry shop page"

	#objList = Product.objects.all()
	objList = Product.objects.filter(isActive = True)

	#featured = request.GET.get("featured")
	#if featured:
	#    objList = objList.filter(featured = True)

	#macrame = request.GET.get("macrame")
	#if macrame:
	#    objList = objList.filter(macrame = True)

	#price_max = request.GET.get("price_max")
	#if price_max:
	#    objList = objList.filter(price__lte = price_max )

	#price_min = request.GET.get("price_min")
	#if price_min:
	#    objList = objList.filter(price__gte = price_min )

	context = {
		"webpage_name":        webpage_name,
		"webpage_description": webpage_description,
		"objList":      objList
	}
	print("\n")
	return render(request, template_name, context)


def product_detail_view(request, id):
	template_name = theme +'/products/detail.html'
	webpage_name = "Product list"
	obj = get_object_or_404(Product, id=id)
	context = {
		"webpage_name": "SKU:" + str(obj.id),
		"obj":          obj
	}
	return render(request, template_name, context)


def product_create_view(request):
	webpage_name = "New product"
	if request.method == "POST":
		print( "\n\nMETHOD IS POST!\n\n" )
		template_name = theme +'/products/list.html'
		title = request.POST.get("title")
		print("Title: {}\n\n".format(title))
		#objList = Product.objects.all()
		objList = Product.objects.filter(title = title)
		context = {
			"webpage_name": webpage_name,
			"objList":      objList
		}
	else:
		print( "\n\nMETHOD IS GET!\n\n" )
		template_name = theme +'/products/create.html'
		form = ProductForm(request.POST or None)
		if form.is_valid():
			form.save()
			form = ProductForm(request.POST or None)

		context = {
			"webpage_name": webpage_name,
			"form":         form
		}
	return render(request, template_name, context)
