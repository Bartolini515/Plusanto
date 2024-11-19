from django import forms
from django.core.validators import MaxLengthValidator, integer_validator



# Formularz dla budżetu
class Budget_form(forms.Form):
    balance = forms.IntegerField(
        label="Saldo konta",
        min_value=0,
        max_value=999999999,
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Wprowadź saldo konta'})
    )
    income = forms.IntegerField(
        label="Dochód",
        min_value=0,
        max_value=999999999,
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Wprowadź dochód'})
    )
    expenses = forms.IntegerField(
        label="Wydatki stałe",
        min_value=0,
        max_value=999999999,
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Wprowadź wydatki stałe'})
    )
    debt = forms.IntegerField(
        label="Dług",
        min_value=0,
        max_value=999999999,
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Wprowadź dług'})
    )
    emergencyFund = forms.IntegerField(
        label="Fundusz awaryjny",
        min_value=0,
        max_value=999999999,
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Wprowadź fundusz awaryjny'})
    )
    budgetType = forms.ChoiceField(
        label="Typ budżetu",
        choices=[('1', 'Stabilny: 50% wydatki / 30% zachcianki / 15% dodatek / 5% awaryjne'), 
                 ('2', 'Rozwojowy: 50% wydatki / 30% dodatek / 20% awaryjne')],
        required=True,
        widget=forms.Select(attrs={'placeholder': 'Wybierz typ budżetu'})
    )
    bufor = forms.IntegerField(
        label="Bufor",
        min_value=0,
        max_value=999999999,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Wprowadź bufor'})
    )
    percentWants = forms.IntegerField(
        label="Procent przekazywany na zachcianki",
        min_value=0,
        max_value=50,
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Wprowadź procent zachcianek'})
    )
    percentAllowance = forms.IntegerField(
        label="Procent przekazywany na dodatek",
        min_value=0,
        max_value=50,
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Wprowadź procent dodatku'})
    )
    percentEmergency = forms.IntegerField(
        label="Procent przekazywany na awaryjność",
        min_value=0,
        max_value=50,
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Wprowadź procent awaryjny'})
    )
    plannedEmergencyFund = forms.IntegerField(
        label="Planowany fundusz awaryjny",
        min_value=0,
        max_value=999999999,
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Wprowadź planowany fundusz awaryjny'})
    )