from django.db import models
from django.urls import reverse

# Create your models here.
class DataFile(models.Model):
	title = models.CharField(max_length=250)
	description = models.CharField(max_length=1000)
	file = models.FileField()

	#def get_absolute_url(self):
	#	return reverse('import')

def __str__(self):
	return self.title + ' - ' +  self.description + ' - ' + self.file
	