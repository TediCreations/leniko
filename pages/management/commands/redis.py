from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import redis


HOSTNAME = settings.REDIS_HOSTNAME
PORT     = settings.REDIS_PORT
PASSWORD = settings.REDIS_PASSWORD


class Command(BaseCommand):
	help = 'Closes the specified poll for voting'

	#def add_arguments(self, parser):
	#	parser.add_argument('poll_ids', nargs='+', type=int)

	def handle(self, *args, **options):
		r = redis.StrictRedis(
			host     = HOSTNAME,
			port     = PORT,
			password = PASSWORD
		)

		rv = None
		try:
			r.set('foo','bar')
			rv = r.get('foo').decode()
		except Exception:
			pass

		if rv != "bar":
			msg = self.style.ERROR(f'FAILED to connect to {HOSTNAME}:{PORT}')
		else:
			msg = self.style.SUCCESS(f'Successfully connected to {HOSTNAME}:{PORT}')

		self.stdout.write(msg)
