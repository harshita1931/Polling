from django.db import models
from django.utils import timezone

# Create your models here.

class MainTable(models.Model):
	userID = models.IntegerField()
	username = models.CharField(max_length=500)
	organizationID = models.IntegerField()


class PreferenceTable(models.Model):
	userID = models.ForeignKey('MainTable')		
	foodID = models.IntegerField()
