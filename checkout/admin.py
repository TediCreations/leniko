from django.contrib import admin

from .models import Order
from .models import OrderItem


class OrderAdmin(admin.ModelAdmin):

	def has_add_permission(self, request):
		return False

	readonly_fields = (
		'ref_code',
		'created_at',
		'isPayed',
		'isDispatched',
		'isRefundAsked',
		'isRefunded'
	)

	list_display = ('ref_code', 'isPayed', 'isDispatched', 'isRefundAsked', 'isRefunded', 'created_at')

	def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
		context.update({
			'show_save': True,
			'show_save_and_continue': False,
			'show_delete': False
		})
		return super().render_change_form(request, context, add, change, form_url, obj)

	list_filter = ('isPayed', 'isDispatched', 'isRefundAsked', 'isRefunded')

	search_fields = ["ref_code"]

	class OrderItemInline(admin.StackedInline):
		model = OrderItem
		extra = 0

	inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):

	def has_add_permission(self, request):
		return False

	readonly_fields = (
		'order',
		'sku',
		'quantity',
		'unit_price'
	)

	list_display = ('order', 'sku', 'quantity', 'unit_price')

	def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
		context.update({
			'show_save': True,
			'show_save_and_continue': False,
			'show_delete': False
		})
		return super().render_change_form(request, context, add, change, form_url, obj)

	search_fields = ["order"]


admin.site.register(OrderItem, OrderItemAdmin)
# admin.site.register(OrderItem)
