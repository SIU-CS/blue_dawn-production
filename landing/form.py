from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class FileForm(forms.Form):
	name = forms.CharField()
	description = forms.CharField(widget=forms.Textarea)
	file = forms.FileField()

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2', )