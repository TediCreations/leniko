#!/usr/bin/env python3

# ------------------------------------------------------------------------------
# Automatically activate the virtual environment
#

# TODO: Should shebang be  ! .venv/bin/python
activate_this = ".venv/bin/activate_this.py"
try:
	with open(activate_this) as f:
		code = compile(f.read(), activate_this, 'exec')
		exec(code, dict(__file__=activate_this))
except Exception:
	print(f"Could not find '{activate_this}'!")
	exit(0)

import os

from invoke import Collection, Config, Exit, task

# ------------------------------------------------------------------------------
# Connect with Django
#

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "leniko.settings")
django.setup()

# ------------------------------------------------------------------------------
# Libraries to import
#

from scripts.populate import registerJewelryVariation
from exportDocx       import export2WholeSaleCatalog
from importProducts   import importData

# ------------------------------------------------------------------------------
# Tasks
#

@task(help={
	"number": "How many entries to add."
})
def populate(ctx, number=10):
	"""Change and inspect the project configurations"""
	if number < 1:
		raise Exception("Number must be bigger that 0!")
	for i in range(number):
		print("---------------------")
		registerJewelryVariation()


@task(help={
	"filepath": "Out document filepath."
})
def wholeSaleCatalog(ctx, filepath="wholesale.docx"):
	"""Generate the wholesale catalog"""
	export2WholeSaleCatalog(filepath)


@task(help={
	"dirpath": "Input directory path."
})
def importProducts(ctx, dirpath=None):
	"""Import products to db"""
	importData(dirpath)


# ------------------------------------------------------------------------------
# Add all tasks to the namespace
ns = Collection(populate, wholeSaleCatalog, importProducts)

# Configure every task to act as a shell command (will print colors,
# allow interactive CLI)
# Add our extra configuration file for the project
config = Config(defaults={"run": {"pty": True}})
ns.configure(config)


def main():
	import sys
	from invoke.main import program
	try:
		sys.exit(program.run())
	except Exception as e:
		print(e)


if __name__ == "__main__":
	main()
