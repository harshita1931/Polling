from django.db import models
from django.utils import timezone

# Create your models here.

class MainTable(models.Model):
	userID = models.ForeignKey('auth.User')
	username = models.CharField(max_length=500)
	organizationID = models.IntegerField()


class PreferenceTable(models.Model):
	userID = models.ForeignKey('auth.User')		
	foodID = models.ForeignKey('FoodItemTable')


class OrganizationTable(models.Model):
	#organizationID = models.IntegerField()
	organizationName = models.CharField(max_length=500) 


class FoodItemTable(models.Model):
	#foodID = models.IntegerField()
	foodName = models.CharField(max_length=500)


class UserExtraDetails(models.Model):
	userID = models.ForeignKey('auth.User')
	organizationName = models.CharField(max_length=500)

