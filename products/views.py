import os

from django.core.paginator          import Paginator
from django.shortcuts               import render
from django.shortcuts               import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http                    import Http404
from django.http                    import HttpResponseRedirect
from django.http                    import HttpResponseBadRequest
from django.http                    import HttpResponseServerError
from django.views                   import View

from .forms  import RingForm
from .forms  import EarringForm
from .forms  import NecklaceForm
from .forms  import BraceletForm

from .models import Product
from .models import ProductTool

from .internal.enum import GroupEnum


from django.conf import settings
from pages.apps  import PagesConfig


theme = PagesConfig.theme


class ProductListView(View):

	"""Show an overview of all available products"""

	template_name = theme + '/shop.html'
	webpage_name = "Shop"
	webpage_description = "Leniko jewelry shop page"

	def get(self, request):

		page_num = 1
		raw_page_num = request.GET.get('page')
		if raw_page_num is not None:
			try:
				page_num = int(raw_page_num)
			except Exception:
				raise Http404("Invalid page number")

		# --------------------------------------------------
		# Objects
		# objList = Product.objects.all()
		objList = Product.objects.filter(isActive=True).order_by('sku')

		# featured = request.GET.get("featured")
		# if featured:
		#    objList = objList.filter(featured = True)

		# macrame = request.GET.get("macrame")
		# if macrame:
		#    objList = objList.filter(macrame = True)

		# price_max = request.GET.get("price_max")
		# if price_max:
		#    objList = objList.filter(price__lte = price_max )

		# price_min = request.GET.get("price_min")
		# if price_min:
		#    objList = objList.filter(price__gte = price_min )

		# --------------------------------------------------
		# Pagination
		productsPerPage = 50
		productPager = Paginator(objList, productsPerPage)

		if 1 > page_num or page_num > productPager.num_pages:
			raise Http404("Page does not exist")

		objList = productPager.page(page_num).object_list
		page = productPager.page(page_num)

		# --------------------------------------------------
		# Render
		context = {
			"webpage_name": self.webpage_name,
			"webpage_description": self.webpage_description,
			"objList": objList,
			"page": page
		}
		return render(request, self.template_name, context)


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

			#def handle_uploaded_file(request, key, destPath):
			#	os.makedirs(destPath, exist_ok = True)
			#	f = None
			#	try:
			#		f = request.FILES[key]
			#	except Exception as e:
			#		return HttpResponseServerError(e)
			#	with open(os.path.join(destPath + str(f)), 'wb+') as destination:
			#	#with open(destPath + str(f), 'wb+') as destination:
			#		for chunk in f.chunks():
			#			destination.write(chunk)
			#
			#handle_uploaded_file(request, 'photo', os.path.join(settings.BASE_DIR, "media/restapi/"))

			def handle_multiuploaded_file(request, key, destPath):
				filePathList = list()
				os.makedirs(destPath, exist_ok = True)
				f_list = request.FILES.getlist(key)
				for f in f_list:
					print(f"File: '{f}'")
					filepath = os.path.join(destPath + str(f))
					filePathList.append(filepath)

					with open(os.path.join(destPath + str(f)), 'wb+') as destination:
						for chunk in f.chunks():
							destination.write(chunk)

				return filePathList


			d = dict(form.cleaned_data)

			filePathList = handle_multiuploaded_file(request, 'photos', os.path.join(settings.BASE_DIR, "media/restapi/"))
			d['photos'] = filePathList

			obj = None
			try:
				obj = ProductTool.createFromForm(d)
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
