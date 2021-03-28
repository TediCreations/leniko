from django.urls import path

from .views import cart_detail
from .views import cart_add
from .views import cart_remove


app_name = 'cart'

urlpatterns = [
	path('', cart_detail, name='detail'),
	path('add_<int:product_id>/', cart_add, name='add'),
	path('remove_<int:product_id>/', cart_remove, name='remove')
]
