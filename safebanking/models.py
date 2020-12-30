from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User_account(models.Model):
	username = models.TextField()
	password = models.TextField()
	balance = models.IntegerField()

