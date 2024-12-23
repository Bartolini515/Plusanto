from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Budget_informations(models.Model): # Model bazy danych budżetu użytkownika
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True)
    balance = models.IntegerField( min("0"))
    income = models.IntegerField( min("0"))
    expenses = models.IntegerField( min("0"))
    debt = models.IntegerField( min("0"))
    emergencyFund = models.IntegerField( min("0"))
    
class Goals(models.Model): # Model bazy danych celów użytkownika
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True)