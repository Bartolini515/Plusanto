from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Informations(models.Model): # Model bazy danych informacji finansowych użytkownika
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True)
    balance = models.IntegerField( min("0"))
    income = models.IntegerField( min("0"))
    expenses = models.IntegerField( min("0"))