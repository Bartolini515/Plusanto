from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Budget_input_informations(models.Model): # Model bazy danych wejściowych budżetu użytkownika
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True)
    balance = models.IntegerField( min("0"))
    income = models.IntegerField( min("0"))
    expenses = models.IntegerField( min("0"))
    debt = models.IntegerField( min("0"))
    emergencyFund = models.IntegerField( min("0"))
    
class Budget_output_informations(models.Model): # Model bazy danych wyjściowych budżetu użytkownika
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True)
    balance = models.IntegerField( min("0"))
    budgetExpenses = models.IntegerField( min("0"))
    budgetWants = models.IntegerField( min("0"))
    allowance = models.IntegerField( min("0"))
    budgetEmergency = models.IntegerField( min("0"))
    debt = models.IntegerField( min("0"))