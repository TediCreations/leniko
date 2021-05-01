from django import forms

from django_countries.fields import CountryField
# from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES = (
	('BD', 'Bank Deposit'),
	('CA', 'Card'),
	('GR', 'Αντικαταβολή'),
	('CW', 'Click away')
)


class BillingForm(forms.Form):

	billing_firstName = forms.CharField(label='Name', required=True, max_length=50, initial=None)
	billing_lastName = forms.CharField(label='Surname', required=True, max_length=50, initial=None)
	billing_phone = forms.CharField(label='Telephone number', required=True, max_length=50, initial=None)
	billing_email = forms.EmailField(label='Email', required=True, initial=None)

	# company_name = forms.CharField(required=False, max_length=50, initial=None)

	billing_address = forms.CharField(label='Address', required=True, max_length=50, initial=None)
	billing_address2 = forms.CharField(label='Address 2', required=False, max_length=50, initial=None)
	billing_city = forms.CharField(label='City', required=True, max_length=50, initial=None)
	billing_state = forms.CharField(label='State', required=False, max_length=50, initial=None)
	"""
	billing_country = CountryField(blank_label='Please select country').formfield(
		required=True,
		widget=CountrySelectWidget(attrs={
			'class': 'custom-select d-block w-100',
		}))
	"""
	billing_country = CountryField(blank_label='Please select country').formfield(required=True, label='Country')
	billing_postalCode = forms.CharField(label='Postal code', required=True, min_length=5, max_length=5, initial=None)

	isShippingAddress = forms.BooleanField(label='Ship to this address?', required=False, initial=True)
	paymentOption = forms.ChoiceField(label='Payment option', choices=PAYMENT_CHOICES, initial=None)

	def store(self):
		if self.is_valid():
			print("\033[92mForm is VALID!!!\033[0m")
			billing_address = self.cleaned_data['billing_address']
			print(f"\033[92mAddress\033[0m : {billing_address}")
		else:
			print("\033[92mForm is VALID!!!\033[0m")
			for e in self.errors:
				print(f"{e}")


class ShippingForm(forms.Form):

	shipping_firstName = forms.CharField(label='Name', required=True, max_length=50, initial=None)
	shipping_lastName = forms.CharField(label='Surname', required=True, max_length=50, initial=None)
	shipping_phone = forms.CharField(label='Telephone number', required=True, max_length=50, initial=None)
	shipping_email = forms.EmailField(label='Email', required=True, initial=None)

	# company_name = forms.CharField(required=False, max_length=50, initial=None)

	shipping_address = forms.CharField(label='Address', required=True, max_length=50, initial=None)
	shipping_address2 = forms.CharField(label='Address 2', required=False, max_length=50, initial=None)
	shipping_city = forms.CharField(label='City', required=True, max_length=50, initial=None)
	shipping_state = forms.CharField(label='State', required=False, max_length=50, initial=None)
	"""
	shipping_country = CountryField(blank_label='Please select country').formfield(
		required=True,
		widget=CountrySelectWidget(attrs={
			'class': 'custom-select d-block w-100',
		}))
	"""
	shipping_country = CountryField(blank_label='Please select country').formfield(required=True, label='Country')
	shipping_postalCode = forms.CharField(label='Postal code', required=True, min_length=5, max_length=5, initial=None)
