from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User_account(models.Model):
	username = models.TextField()
	password = models.TextField()
	balance = models.IntegerField()
	motto = models.TextField(default = "")
	account_number = models.TextField(default = "1234-5678")
	status = models.IntegerField(default = 1) #1 = normal user, 2 = admin user

