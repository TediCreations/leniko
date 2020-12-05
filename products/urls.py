from django.urls import path

from .views import product_list_view
from .views import product_create_view
from .views import product_detail_view


app_name = 'products'

urlpatterns = [
	path(''              , product_list_view  , name='product'),
	path('create'        , product_create_view, name='product-create'),
	path('sku_<int:id>/' , product_detail_view, name='product-detail'),
]
