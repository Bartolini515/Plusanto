from django import forms
from .models import Informations



# Formularz z polami: Balans konta, Dochód, Wydatki stałe
class Informations_form(forms.Form):
    balance = forms.IntegerField(
        label="Balans konta",
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Wprowadź balans konta'}))
    income = forms.IntegerField(
        label="Dochód",
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Wprowadź dochód'}))
    expenses = forms.IntegerField(
        label="Wydatki stałe",
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Wprowadź wydatki stałe'}))