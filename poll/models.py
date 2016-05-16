from django.db import models
from django.utils import timezone

# Create your models here.

class PreferenceTable(models.Model):
	userID = models.ForeignKey('auth.User')		
	foodID = models.ForeignKey('FoodItemTable')


class OrganizationTable(models.Model):
	organizationName = models.CharField(max_length=500) 


class FoodItemTable(models.Model):
	foodName = models.CharField(max_length=500)


class UserExtraDetails(models.Model):
	userID = models.ForeignKey('auth.User')
	organizationName = models.CharField(max_length=500)