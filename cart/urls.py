from django.urls import path

from .views import cart_detail
from .views import cart_add
from .views import cart_remove


app_name = 'cart'

urlpatterns = [
	path('', cart_detail, name='cart-detail'),
	path('add_<int:product_id>/', cart_add, name='cart-add'),
	path('remove_<int:product_id>/', cart_remove, name='cart-remove'),
]
