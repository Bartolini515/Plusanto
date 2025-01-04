from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .forms import Budget_form, CalculatorForm, AffordabilityForm
from .models import Budget_input_informations, Budget_output_informations
from django.http import JsonResponse
from .algorithms import budgetRule, affordabilityRule
from json import dumps

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
            debt = form.cleaned_data['debt'] or 0
            emergencyFund = form.cleaned_data['emergencyFund'] or 0
            budgetType = form.cleaned_data['budgetType']
            bufor = form.cleaned_data['bufor'] or 0
            percentWants = form.cleaned_data['percentWants'] or 0
            percentAllowance = form.cleaned_data['percentAllowance'] or 0
            percentEmergency = form.cleaned_data['percentEmergency'] or 0
            plannedEmergencyFund = form.cleaned_data['plannedEmergencyFund'] or 0
            
            try:
                Budget_input_informations.objects.get(pk=request.user) # Sprawdzamy czy użytkownik ma już informacje
                Budget_input_informations.objects.filter(pk=request.user).update(balance=balance, income=income, expenses=expenses, debt=debt, emergencyFund=emergencyFund) # Aktualizujemy rekordy
            except Budget_input_informations.DoesNotExist: # Jeżeli użytkownik pierwszy raz wprowadza informacje, wpisujemy go do bazy danych jak nowego
                budget = Budget_input_informations.objects.create(user=request.user, balance=balance, income=income, expenses=expenses, debt=debt, emergencyFund=emergencyFund) # Tworzymy rekordy
                budget.save()
            
            balance, budgetExpenses, budgetWants, allowance, budgetEmergency, debt, messagesArray, lackingFunds = budgetRule(
                balance, income, expenses, debt, emergencyFund, budgetType, bufor, percentWants, percentAllowance, percentEmergency, plannedEmergencyFund, distributeConf)
            
            if lackingFunds:
                return JsonResponse({'status': 'error', 'message': 'Brak wystarczających środków.'})
            
            labels = ['Budżet wydatkowy', 'Dodatek', 'Budżet awaryjny']
            values = [budgetExpenses, allowance, budgetEmergency]
            if budgetType == '1':
                labels.insert(1, 'Budżet zachcianek')
                values.insert(1, budgetWants)
            
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
                'labels': labels,
                'values': values,
                }) 
            
            try:
                Budget_output_informations.objects.get(pk=request.user) # Sprawdzamy czy użytkownik ma już informacje
                Budget_output_informations.objects.filter(pk=request.user).update(balance=balance, budgetExpenses=budgetExpenses, budgetWants=budgetWants, allowance=allowance, budgetEmergency=budgetEmergency, debt=debt) # Aktualizujemy rekordy
            except Budget_output_informations.DoesNotExist: # Jeżeli użytkownik pierwszy raz wprowadza informacje, wpisujemy go do bazy danych jak nowego
                budget = Budget_output_informations.objects.create(user=request.user, balance=balance, budgetExpenses=budgetExpenses, budgetWants=budgetWants, allowance=allowance, budgetEmergency=budgetEmergency, debt=debt) # Tworzymy rekordy
                budget.save()
            
            
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
            budget = Budget_input_informations.objects.get(user=request.user)
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
        except Budget_input_informations.DoesNotExist:
            form = Budget_form()
        
        try: # Sprawdzamy czy użytkownika posiada informacje wyjściowe, jeżeli tak to dajemy do JSONa
            budget = Budget_output_informations.objects.get(pk=request.user)
            
            labels = ['Budżet wydatkowy', 'Dodatek', 'Budżet awaryjny']
            values = [budget.budgetExpenses, budget.allowance, budget.budgetEmergency]
            if budgetType == '1':
                labels.insert(1, 'Budżet zachcianek')
                values.insert(1, budget.budgetWants)
            
            data = {
                'balance': budget.balance,
                'budgetExpenses': budget.budgetExpenses,
                'budgetWants': budget.budgetWants,
                'allowance': budget.allowance,
                'budgetEmergency': budget.budgetEmergency,
                'debt': budget.debt,
                'labels': labels,
                'values': values,
            }
            dataJSON = dumps(data)
        except Budget_output_informations.DoesNotExist:
            dataJSON = False
            
    return render(request, 'budget.html', {'form': form, 'dataJSON': dataJSON}) # Jeżeli użytkownik nie wysyła żadnych danych to wyświetli stronę informacji

def about(request): # O nas
    return render(request, 'about.html')

def contact(request): # Kontakt
    return render(request, 'contact.html')

def calculator(request): # Kalkulator
    form = CalculatorForm()
    return render(request, 'calculator.html', {'form': form})

def affordability(request): # Przystępnościomierz
    if request.method == 'POST': # Sprawdzamy czy użytkownik przesyła dane
        form = AffordabilityForm(request.POST)
        action = request.POST.get('action')
        if form.is_valid() and action == 'calculate':  # Sprawdzamy czy formularz jest poprawny
            # Wyciągamy dane z formularza
            expense = form.cleaned_data['expense']
            frequency = form.cleaned_data['frequency']
            
            budgetType = request.COOKIES.get('budgetType', '1')
            
            budget_in = Budget_input_informations.objects.get(user=request.user)
            income = budget_in.income
            budget_out = Budget_output_informations.objects.get(user=request.user)
            balance = budget_out.balance
            budgetExpenses = budget_out.budgetExpenses
            budgetWants = budget_out.budgetWants
            allowance = budget_out.allowance
            
            balanceAft, budgetExpensesAft, budgetWantsAft, allowanceAft, canDo, messagesArray, labels, values = affordabilityRule(income, balance, budgetExpenses, budgetWants, allowance, expense, frequency, budgetType)
            
            # Zwróć odpowiedź dla strony o udanym zapisie danych oraz wartości dla strony
            response = JsonResponse({
                'status': 'success', 
                'message': 'Obliczenia wykonane poprawnie.',
                'balance': int(balance),
                'budgetExpenses': int(budgetExpenses),
                'budgetWants': int(budgetWants),
                'allowance': int(allowance),
                'balanceAft': int(balanceAft),
                'budgetExpensesAft': int(budgetExpensesAft),
                'budgetWantsAft': int(budgetWantsAft),
                'allowanceAft': int(allowanceAft),
                'messages': messagesArray,
                'canDo': canDo,
                'labels': labels,
                'values': values,
                }) 
            return response
        elif action == 'save':
            balanceAft = request.POST.get('balanceAft')
            budgetExpensesAft = request.POST.get('budgetExpensesAft')
            budgetWantsAft = request.POST.get('budgetWantsAft')
            allowanceAft = request.POST.get('allowanceAft')
            
            Budget_output_informations.objects.filter(pk=request.user).update(balance=balanceAft, budgetExpenses=budgetExpensesAft, budgetWants=budgetWantsAft, allowance=allowanceAft) # Aktualizujemy rekordy
            return JsonResponse({'status': 'success', 'message': 'Zapisano dane.'})
        else:
            # Zwróć odpowiedź dla strony o niepoprawnym formularzu
            return JsonResponse({'status': 'error', 'message': 'Niepoprawny format danych.'})
    else:
        try: # Sprawdzamy czy użytkownik ma już informacje wyjściowe budżetu
            Budget_output_informations.objects.get(pk=request.user) 
            form = AffordabilityForm()
            return render(request, 'affordability.html', {'form': form}) # Jeżeli użytkownik nie wysyła żadnych danych to wyświetli stronę informacji
        except Budget_output_informations.DoesNotExist: # Jeżeli nie posiada to odmawiamy dostępu
            messages.error(request, 'Musisz najpierw obliczyć budżet aby skorzystać z przystępnościomierza.')
            return redirect('dashboard')