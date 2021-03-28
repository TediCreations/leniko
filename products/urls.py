from django.urls import path

from .views import ProductListView
from .views import product_create_view
from .views import product_detail_view


app_name = 'products'

urlpatterns = [
	path('', ProductListView.as_view(), name='list'),
	path('sku_<int:id>/', product_detail_view, name='detail'),
	path('create', product_create_view, name='create')
]
