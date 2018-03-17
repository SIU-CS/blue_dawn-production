from django.db import models
from django.urls import reverse
#from .validators import validate_file_extension
from django.contrib.auth.models import User
from jsonfield import JSONField

class DataSet(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	data = JSONField() 

class DataFile(models.Model):
	#title = models.CharField(max_length=250)
	#description = models.CharField(max_length=1000)
	file = models.FileField(upload_to = '%Y/%m/%d')

def __str__(self):
	return self.file