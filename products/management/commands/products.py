from django.core.management.base import BaseCommand, CommandError
from products.models import Product


class Command(BaseCommand):

	help = 'Work with products'

	def add_arguments(self, parser):
		parser.add_argument('-b', '--bracelet', action='store_true', help='Select bracelet jewelry')
		parser.add_argument('-r', '--ring', action='store_true', help='Select ring jewelry')
		parser.add_argument('-n', '--necklace', action='store_true', help='Select necklace jewelry')
		parser.add_argument('-e', '--earring', action='store_true', help='Select earring jewelry')
		parser.add_argument('-s', '--silver925', action='store_true', help='Select Silver 925 jewelry')
		parser.add_argument('-m', '--macrame', action='store_true', help='Select macrame jewelry')

	def handle(self, *args, **options):

		if options['bracelet'] is True:
			objList = Product.objects.bracelets()
		elif options['ring'] is True:
			objList = Product.objects.rings()
		elif options['necklace'] is True:
			objList = Product.objects.necklaces()
		elif options['earring'] is True:
			objList = Product.objects.earrings()
		elif options['silver925'] is True:
			objList = Product.objects.silver925()
		elif options['macrame'] is True:
			objList = Product.objects.macrame()
		else:
			objList = Product.objects.active()

		if objList is None:
			raise CommandError('Does not exist')

		for obj in objList:
			self.stdout.write(f"{obj.id:<5}: {obj.jewelry.getTitle():<50} {obj.price}")

		objLen = len(objList)
		self.stdout.write(self.style.SUCCESS(f"Found {objLen} products"))
