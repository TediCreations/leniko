from django import forms


class ContactForm(forms.Form):

	name = forms.CharField(label='Name', required=True, max_length=50, initial=None)
	email = forms.EmailField(label='Email', required=True, initial=None)
	message = forms.CharField(label='Message', widget=forms.Textarea, required=True, max_length=300, initial=None)

	# newsletter = forms.BooleanField(label='', required=False, initial=True)
