from django.shortcuts               import render
from django.shortcuts               import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http                    import HttpResponseRedirect
from django.http                    import HttpResponseBadRequest
from django.http                    import HttpResponseServerError

from .forms  import RingForm
from .forms  import EarringForm
from .forms  import NecklaceForm
from .forms  import BraceletForm

from .models import Product
from .models import ProductTool

from .internal.enum import GroupEnum

from leniko.settings import BASE_DIR
from pages.apps      import PagesConfig


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
	template_name = theme + '/product-details.html'
	webpage_name = "Product list"
	obj = get_object_or_404(Product, id=id)
	context = {
		"webpage_name": "SKU:" + str(obj.id),
		"obj":          obj
	}
	return render(request, template_name, context)


@user_passes_test(lambda u: u.is_superuser)
def product_create_view(request, *args, **kwargs):

	group = "None"

	msg = None
	if request.method == 'POST':
		msg = request.POST
		group = request.POST.get('group')
		if group == GroupEnum.RI.value:
			form = RingForm(request.POST, request.FILES)
		elif group == GroupEnum.BR.value:
			form = BraceletForm(request.POST, request.FILES)
		elif group == GroupEnum.NE.value:
			form = NecklaceForm(request.POST, request.FILES)
		elif group == GroupEnum.EA.value:
			form = EarringForm(request.POST, request.FILES)
		else:
			form = None
			return HttpResponseBadRequest("Group is invalid")

		if form.is_valid():

			import os
			def handle_uploaded_file(request, key, destPath):
				if not os.path.exists(destPath):
					os.mkdir(destPath)
				f = request.FILES[key]
				with open(os.path.join(destPath + str(f)), 'wb+') as destination:
				#with open(destPath + str(f), 'wb+') as destination:
					for chunk in f.chunks():
						destination.write(chunk)

			handle_uploaded_file(request, 'photo2', os.path.join(BASE_DIR, "media/restapi/"))


			obj = None
			try:
				obj = ProductTool.createFromForm(form)
			except Exception as e:
				return HttpResponseServerError(e)

			return HttpResponseRedirect(obj.get_absolute_url())

	else:
		group = request.GET.get('group')

		form = None
		if group == GroupEnum.RI.value:
			form = RingForm()
		elif group == GroupEnum.BR.value:
			form = BraceletForm()
		elif group == GroupEnum.NE.value:
			form = NecklaceForm()
		elif group == GroupEnum.EA.value:
			form = EarringForm()
		else:
			form = None

	template_name = theme + '/product-create.html'
	webpage_name = "Create product"
	webpage_description = "Leniko jewelry create product"

	context = {
		"webpage_name":        webpage_name,
		"webpage_description": webpage_description,
		"message":             msg,
		"form":                form,
		"group":               group
	}
	return render(request, template_name, context)
