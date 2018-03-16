from django.db import models
from django.urls import reverse
from .validators import validate_file_extension
import csv
#import openpyxl
#import xmltodict
from dicttoxml import dicttoxml
import dicttoxml


# Create your models here.



class DataFile(models.Model):
	title = models.CharField(max_length=250)
	description = models.CharField(max_length=1000)
	file = models.FileField()#validators=[validate_file_extension])

	"""def save(self, *args, **kwargs):
		if self.file:
			#if filetype == FileType.CSV:
			  with open('media/*.xml', newline='') as csv_file:
				  csv_data = csv.reader(self.file)
				  xml_dict = dict()
				  xml_dict["tags"] = list()
				  xml_dict["data"] = list()
  
				  xml_dict["title"] = csv_data.__next__()
				  xml_dict["description"] = csv_data.__next__()
  
				  for row in csv_data:
					  data_item = dict()
					  data_item["question"] = row[0]
					  data_item["tag"] = str()
					  xml_dict["data"].append(data_item)
				  
			  self.xml = dicttoxml(xml_dict)
  
		super(DataFile, self).save(*args, **kwargs)"""
	#def get_absolute_url(self):
	#	return reverse('index')

def __str__(self):
	return self.title + ' - ' +  self.description + ' - ' + self.file
	