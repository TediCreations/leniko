from django.contrib import admin

# Register your models here.
from .models import Cart
from .models import CartItem


admin.site.register(Cart)
admin.site.register(CartItem)
