from django.contrib import admin
from django.urls import path
from django.urls import include

from django.conf import settings
from django.conf.urls.static import static

from pages.views import login_view
from pages.views import logout_view
from pages.views import HomeView
from pages.views import AboutView
from pages.views import ContactView

urlpatterns = [
	path('', HomeView.as_view(), name='home'),
	path('login/', login_view, name='login'),
	path('logout/', logout_view, name='logout'),
	path('about/', AboutView.as_view(), name='about'),
	path('contact/', ContactView.as_view(), name='contact'),

	path('dev/', include('dev.urls')),
	path('product/', include('products.urls')),
	path('cart/', include('cart.urls')),
	path('checkout/', include('checkout.urls')),

	path('admin/login/', login_view, name='admin-login'),
	path('admin/', admin.site.urls, name='admin'),
]

handler400 = 'pages.views.handler400'
handler404 = 'pages.views.handler404'
handler500 = 'pages.views.handler500'

if settings.DEBUG is True:
	import debug_toolbar
	urlpatterns.append(path('debug/', include(debug_toolbar.urls)))

if settings.DEBUG is True:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Admin page title
admin.site.site_header = "Leniko Jewelry"

# Modify Site Header
admin.site.index_title = 'Leniko Jewelry'
# Modify Site Title
admin.site.site_title = 'Administration'
