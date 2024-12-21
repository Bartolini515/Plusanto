from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .forms import Budget_form
from .models import Informations
from django.http import JsonResponse
from .algorithms import budgetRule

def index(request): # Strona główna
    return render(request, 'index.html')

#TODO: Akceptacja cookies https://medium.com/@kanithkar_baskaran/how-to-save-cookies-in-web-django-847136032737

def dashboard(request): # Pulpit
    if  request.user.is_authenticated:
        return render(request, 'dashboard.html')
    else:
        messages.info(request, "Aby wejść do pulpitu musisz się najpierw zalogować.")
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    
def budget(request): # Sekcja budżetu
    if request.method == 'POST': # Sprawdzamy czy użytkownik przesyła dane
        form = Budget_form(request.POST)
        if form.is_valid():  # Sprawdzamy czy formularz jest poprawny
            # Wyciągamy dodatkowe dane w AJAXie
            distributeConf = request.POST.get('distributeConf', 'false') == 'true'
            # Wyciągamy dane z formularza
            balance = form.cleaned_data['balance']
            income = form.cleaned_data['income']
            expenses = form.cleaned_data['expenses']
            debt = form.cleaned_data['debt']
            emergencyFund = form.cleaned_data['emergencyFund']
            budgetType = form.cleaned_data['budgetType']
            bufor = form.cleaned_data['bufor']
            percentWants = form.cleaned_data['percentWants']
            percentAllowance = form.cleaned_data['percentAllowance']
            percentEmergency = form.cleaned_data['percentEmergency']
            plannedEmergencyFund = form.cleaned_data['plannedEmergencyFund']
            
            try:
                Informations.objects.get(pk=request.user) # Sprawdzamy czy użytkownik ma już informacje
                Informations.objects.filter(pk=request.user).update(balance=balance, income=income, expenses=expenses, debt=debt, emergencyFund=emergencyFund) # Aktualizujemy rekordy
            except Informations.DoesNotExist: # Jeżeli użytkownik pierwszy raz wprowadza informacje, wpisujemy go do bazy danych jak nowego
                budget = Informations.objects.create(user=request.user, balance=balance, income=income, expenses=expenses, debt=debt, emergencyFund=emergencyFund) # Tworzymy rekordy
                budget.save()
            
            balance, budgetExpenses, budgetWants, allowance, budgetEmergency, debt, messagesArray = budgetRule(
                balance, income, expenses, debt, emergencyFund, budgetType, bufor, percentWants, percentAllowance, percentEmergency, plannedEmergencyFund, distributeConf)
            
            # Zwróć odpowiedź dla strony o udanym zapisie danych oraz wartości dla pól budżetu
            response = JsonResponse({
                'status': 'success', 
                'message': 'Dane zostały zapisane.',
                'balance': int(balance),
                'budgetExpenses': int(budgetExpenses),
                'budgetWants': int(budgetWants),
                'allowance': int(allowance),
                'budgetEmergency': int(budgetEmergency),
                'debt': int(debt),
                'messages': messagesArray,
                }) 
            
            # Deklarujemy ciasteczka z pozostałych wartości które warto zapisać
            response.set_cookie(key='budgetType', value=str(budgetType), max_age=60*60*24*365)
            response.set_cookie(key='bufor', value=str(bufor), max_age=60*60*24*365)
            response.set_cookie(key='percentWants', value=str(percentWants), max_age=60*60*24*365)
            response.set_cookie(key='percentAllowance', value=str(percentAllowance), max_age=60*60*24*365)
            response.set_cookie(key='percentEmergency', value=str(percentEmergency), max_age=60*60*24*365)
            response.set_cookie(key='plannedEmergencyFund', value=str(plannedEmergencyFund), max_age=60*60*24*365)
            return response
        else:
            # Zwróć odpowiedź dla strony o niepoprawnym formularzu
            return JsonResponse({'status': 'error', 'message': 'Niepoprawny format danych.'})
    else:
        try: # Sprawdzamy czy użytkownik posiada informacje, jeżeli tak wyświetlamy je jako wartości formularza
            budget = Informations.objects.get(user=request.user)
            budgetType = request.COOKIES.get('budgetType', '1')
            bufor = request.COOKIES.get('bufor', '')
            percentWants = request.COOKIES.get('percentWants', '30')
            percentAllowance = request.COOKIES.get('percentAllowance', '15')
            percentEmergency = request.COOKIES.get('percentEmergency', '5')
            plannedEmergencyFund = request.COOKIES.get('plannedEmergencyFund', '')

            # Ustalamy wartości początkowe na te wcześniej zapisane
            form = Budget_form(initial={
                'balance': budget.balance,
                'income': budget.income,
                'expenses': budget.expenses,
                'debt': budget.debt,
                'emergencyFund': budget.emergencyFund,
                'budgetType': budgetType,
                'bufor': bufor,
                'percentWants': percentWants,
                'percentAllowance': percentAllowance,
                'percentEmergency': percentEmergency,
                'plannedEmergencyFund': plannedEmergencyFund,
            })
        except Informations.DoesNotExist:
            form = Budget_form()
    return render(request, 'budget.html', {'form': form}) # Jeżeli użytkownik nie wysyła żadnych danych to wyświetli stronę informacji

def about(request): # O nas
    return render(request, 'about.html')

def contact(request): # Kontakt
    return render(request, 'contact.html')

def calculator(request): # Kalkulator
    return render(request, 'calculator.html')

def goals(request): # Cele
    return render(request, 'goals.html')