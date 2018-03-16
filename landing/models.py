from django.db import models
from django.urls import reverse
from .validators import validate_file_extension
from django.contrib.auth.models import User

class DataSet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=30)
    data = models.BinaryField(blank=True) 



