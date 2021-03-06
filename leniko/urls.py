"""leniko URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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

from pages.views import dev_view
from pages.views import dev_form
from pages.views import dev_coming_soon
from pages.views import handler400
from pages.views import handler404
from pages.views import handler500


urlpatterns = [
	path(''            , HomeView.as_view()    , name='home'),

	path('login/'      , login_view            , name='login'),
	path('logout/'     , logout_view           , name='logout'),
	path('about/'      , AboutView.as_view()   , name='about'),
	path('contact/'    , ContactView.as_view() , name='contact'),

	path('product/'    , include('products.urls')),
	path('cart/'       , include('cart.urls')),

	path('dev/'        , dev_view              , name='dev'),
	path('coming-soon/', dev_coming_soon       , name='coming-soon'),
	path('dev/form/'   , dev_form              , name='dev'),
	path('dev/400/'    , handler400            , name='dev'),
	path('dev/404/'    , handler404            , name='dev'),
	path('dev/500/'    , handler500            , name='dev'),

	path('admin/login/', login_view            , name='admin-login'),
	path('admin/'      , admin.site.urls       , name='admin'),
]

handler400 = 'pages.views.handler400'
handler404 = 'pages.views.handler404'
handler500 = 'pages.views.handler500'

if settings.DEBUG is True:
	import debug_toolbar
	urlpatterns.append(path('debug/' , include(debug_toolbar.urls)))

if settings.DEBUG is True:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Admin page title
admin.site.site_header = "Leniko Jewelry"

# Modify Site Header
admin.site.index_title = 'Leniko Jewelry'
# Modify Site Title
admin.site.site_title = 'Administration'
