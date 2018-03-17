from django import forms



class FileForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    file = forms.FileField()
