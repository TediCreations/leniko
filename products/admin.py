from django.contrib    import admin
from django.utils.html import format_html
from django.contrib    import messages

# Register your models here.
from .models import Bracelet
from .models import Necklace
from .models import Ring
from .models import Earring
from .models import JewelryGroup
from .models import Jewelry
from .models import JewelryPhoto
from .models import JewelryColor
from .models import Product

import os

admin.site.register(Bracelet)
admin.site.register(Necklace)
admin.site.register(Ring)
admin.site.register(Earring)
admin.site.register(JewelryGroup)
#admin.site.register(Jewelry)
#admin.site.register(JewelryPhoto)
#admin.site.register(JewelryColor)
#admin.site.register(Product)


# Globally disable delete selected
#admin.site.disable_action('delete_selected')


class JewelryAdmin(admin.ModelAdmin):
	def photo_tag(self, obj):
		return format_html(f'<img src="{obj.photo}" width="35" height="35" >')
	photo_tag.short_description = 'Photo'

	list_display = ('getTitle', 'material', 'platting', 'group')

	class JewelryInline(admin.StackedInline):
		model = JewelryPhoto
		extra = 0

	#fieldsets = [
	#	('Variation',        {'fields': ['material']}),
	#	('Variation',        {'fields': ['platting']}),
	#	('Variation',        {'fields': ['photos']}),
	#]
	inlines = [JewelryInline]

admin.site.register(Jewelry, JewelryAdmin)


class JewelryPhotoAdmin(admin.ModelAdmin):
	def photo_tag(self, obj):
		return format_html(f'<img src="{obj.photo}" width="35" height="35" >')
	photo_tag.short_description = 'Photo'

	list_display = ('photo_tag', 'priority', 'jewelry')

admin.site.register(JewelryPhoto, JewelryPhotoAdmin)


class JewelryColorAdmin(admin.ModelAdmin):
	def photo_tag(self, obj):
		return format_html(f'<img src="{obj.getPhotoUrl()}" width="35" height="35" >')
	photo_tag.short_description = 'Photo'

	list_display = ('photo_tag', 'color', 'jewelry')

admin.site.register(JewelryColor, JewelryColorAdmin)


class ProductAdmin(admin.ModelAdmin):

	#def has_change_permission(self, request, obj=None):
	#	"""Disable edit"""
	#	#if obj is not None and obj.status > 1:
	#	return False
	#	#return super().has_change_permission(request, obj=obj)

	def activate(modeladmin, request, queryset):
		l = len(queryset)
		for product in queryset:
			product.isActive = True
			product.save()
		messages.add_message(request, messages.INFO, f"Activated {l} products.")


	def deactivate(modeladmin, request, queryset):
		l = len(queryset)
		for product in queryset:
			product.isActive = False
			product.save()
		messages.add_message(request, messages.INFO, f"Deactivated {l} products.")

	def export(modeladmin, request, queryset):
		"""Action to export selected products"""

		# Delete directory
		#baseDirPath = os.path.join(os.getcwd(), "static/export/")
		baseDirPath = os.path.join("/tmp/", "lenikoExport")
		import shutil
		try:
			shutil.rmtree(baseDirPath)
		except FileNotFoundError:
			pass

		# Create directory
		if not os.path.isdir(baseDirPath):
			try:
				os.mkdir(baseDirPath)
			except OSError:
				messages.add_message(request, messages.ERROR, f"Creation of the directory '{baseDirPath}' failed.")
				return
		else:
			messages.add_message(request, messages.ERROR, f"Deletion of directory '{baseDirPath}' failed.")

		# Export
		# For each product in the query
		for product in queryset:
			# Name in the list
			listFilePath = os.path.join(baseDirPath, "list.txt")
			listFile = open(listFilePath, "w")
			txt  = ""
			txt += f"Name:        {product}\n"
			txt += f"Title:       {product.getTitle()}\n"
			txt += f"sku:         {product.sku}\n"
			txt += f"price:       {product.price}\n"
			txt += f"isFeatured:  {product.isFeatured}\n"
			txt += f"isActive:    {product.isActive}\n"
			txt += f"\n"
			txt += f"Brief:       {product.jewelry.getBrief()}\n"
			txt += f"Description: {product.jewelry.getDescription()}\n"
			#txt += f"Photos:\n"
			#for photo in product.getPhotoList():
			#	photoPath = os.path.join(os.getcwd(), str(photo['url']))
			#	txt += f"Photo:       {photo['priority']} | {photoPath}\n"
			txt += f"Variations:\n"
			txt += f"Variation1: {product.jewelry.group}\n"
			txt += f"Variation2: {JewelryGroup.objects.all()}\n"
			txt += f"Variation3: {JewelryGroup.objects.filter(id=product.jewelry.group.id)}\n"
			#for jewelryGroup in JewelryGroup.objects.filter(id=product.jewelry.group.id):
			for variation in Jewelry.objects.filter(group=product.jewelry.group):
				no = str(variation)
				txt += f"Variation-:  {no}\n"
			jewelryGroup = Jewelry.objects.filter(group=product.jewelry.group)
			#Jewelry.objects.Group.all()
			txt += f"\n"

			# Create jewelry group directory
			group = product.jewelry.getGroup()
			groupDirPath = os.path.join(baseDirPath, group)
			if not os.path.isdir(groupDirPath):
				try:
					os.mkdir(groupDirPath)
				except OSError:
					messages.add_message(request, messages.ERROR, f"Creation of the directory '{groupDirPath}' failed.")
					break

			# Create jewelry directory
			group = product.jewelry.getGroup()
			name = product.getTitle().replace(" ", "_")
			jewelryDirPath = os.path.join(baseDirPath, group, name)
			if not os.path.isdir(jewelryDirPath):
				try:
					os.mkdir(jewelryDirPath)
				except OSError:
					messages.add_message(request, messages.ERROR, f"Creation of the directory '{jewelryDirPath}' failed.")
					break

			# Create jewelry variation directory
			#variationNo = str()
			#for jewelryVariation in product.jewelry.
			#jewelryVariationDirPath = os.path.join(jewelryDirPath, variationNo)
			#if not os.path.isdir(jewelryDirPath):
			#	try:
			#		os.mkdir(jewelryDirPath)
			#	except OSError:
			#		messages.add_message(request, messages.ERROR, f"Creation of the directory '{jewelryDirPath}' failed.")
			#		break
			filePath = os.path.join(jewelryDirPath, "variations.txt")
			f = open(filePath, "a")
			f.write(txt)
			f.close()

			# Copy photos
			for photo in product.getPhotoList():
				no = str(photo['no'])
				sourcePhotoPath = os.path.join(os.getcwd(), str(photo['url']))
				extension = os.path.splitext(sourcePhotoPath)[1]
				destinationPhotoPath = os.path.join(jewelryDirPath, no + "_" + "photo" + extension)

				try:
					shutil.copyfile(sourcePhotoPath, destinationPhotoPath)
					pass
				except IOError:
					messages.add_message(request, messages.ERROR, f"Failed to copy to '{destinationPhotoPath}'.")
					break

		#print ("Successfully created the directory %s " % path)
		# DEBUG
		# INFO
		# SUCCESS
		# WARNING
		# ERROR
		n = len(queryset)
		txt = f"Exported {n} products to {baseDirPath} successfully."
		messages.add_message(request, messages.INFO, txt)
	export.short_description = "Export"

	def photo_tag(self, obj):
		return format_html(f'<img src="{obj.getPhotoUrl()}" width="35" height="35" >')
	photo_tag.short_description = 'Photo'

	list_display = ('photo_tag', 'getTitle', 'sku', 'isFeatured', 'isActive', 'price', 'jewelry')

	#ordering = ['isFeatured']
	actions = [activate, deactivate, export]

	fieldsets = [
		("Product info", {
			'fields': ['sku', 'price', ('isFeatured', 'isActive')]
		}),
		('Jewelry Info',     {
			'classes': ('extrapretty',),
			'fields': ['jewelry'],
			#'legend': ("FUCK")
		}),
	]

	list_filter = ('isFeatured', 'isActive')

	#search_fields = ("sku", "isFeatured" )

admin.site.register(Product, ProductAdmin)
