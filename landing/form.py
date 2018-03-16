from django import forms
from .models import DataFile
import dicttoxml


class FileForm(forms.ModelForm):
	class Meta:
		model = DataFile
		fields = ['title', 'description', 'file']

	