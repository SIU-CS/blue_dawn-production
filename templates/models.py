from django.db import models
from django.urls import reverse
#from .validators import validate_file_extension
from django.contrib.auth.models import User
from jsonfield import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver

class DataSet(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	data = JSONField() 

class Confirm(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	confirmation = models.BooleanField(default = False)

@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
	if created:
		Confirm.objects.create(user=instance)
	instance.confirm.save()