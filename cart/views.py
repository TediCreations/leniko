from django.shortcuts import render, redirect, get_object_or_404

from .models import Cart

from .forms import CartAddProductForm

from products.models import Product

from pages.apps import PagesConfig


theme = PagesConfig.theme


def cart_detail(request):

	if request.method == 'POST':
		print(f"request: {request.POST}")
		print(f"request: {request.POST.get('input-qty')}")
		print("")

	template_name = theme + '/shopping-cart.html'
	webpage_name = "Shopping cart"
	webpage_description = "Leniko jewelry shopping cart page"

	cart = Cart(request)

	context = {
		"webpage_name": webpage_name,
		"webpage_description": webpage_description,
		"cart": cart
	}
	return render(request, template_name, context)


def cart_add(request, product_id):

	product = get_object_or_404(Product, id=product_id)
	cart = Cart(request)

	if request.method == 'GET':
		cart.add(product=product)
	else:
		form = CartAddProductForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])

	return redirect('cart:cart-detail')


def cart_remove(request, product_id):

	cart = Cart(request)

	product = get_object_or_404(Product, id=product_id)
	cart.remove(product)
	return redirect('cart:cart-detail')
