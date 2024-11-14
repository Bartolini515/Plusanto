from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .forms import Informations_form
from .models import Informations

def index(request): # Strona główna
    return render(request, 'index.html')

def dashboard(request): # Pulpit
    if  request.user.is_authenticated:
        return render(request, 'dashboard.html')
    else:
        messages.info(request, "Aby wejść do pulpitu musisz się najpierw zalogować.")
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    
def informations(request): # Informacje finansowe o użytkowniku
    if request.method == 'POST': # Sprawdzamy czy użytkownik przesyła dane
        form = Informations_form(request.POST)
        if form.is_valid():  # Sprawdzamy czy formularz jest poprawny
            balance = form.cleaned_data['balance']
            income = form.cleaned_data['income']
            expenses = form.cleaned_data['expenses']
            try:
                Informations.objects.get(pk=request.user) # Sprawdzamy czy użytkownik ma już informacje
                Informations.objects.filter(pk=request.user).update(balance=balance, income=income, expenses=expenses) # Aktualizujemy rekordy
            except Informations.DoesNotExist: # Jeżeli użytkownik pierwszy raz wprowadza informacje, wpisujemy go do bazy danych jak nowego
                informations = Informations.objects.create(user=request.user, balance=balance, income=income, expenses=expenses) # Tworzymy rekordy
                informations.save()
            return redirect('informations')
    else:
        try: # Sprawdzamy czy użytkownik posiada informacje, jeżeli tak wyświetlamy je jako wartości formularza
            informations = Informations.objects.get(user=request.user)
            form = Informations_form(initial={'balance': informations.balance, 'income': informations.income, 'expenses': informations.expenses})
        except Informations.DoesNotExist:
            form = Informations_form()
        # informations = Informations.objects.get(pk=request.user)
        # balance = informations.balance
        # income = informations.income
        # expenses = informations.expenses




    return render(request, 'informations.html', {'form': form}) # Jeżeli użytkownik nie wysyła żadnych danych to wyświetli stronę informacji

def about(request): # O nas
    return render(request, 'about.html')

def contact(request): # Kontakt
    return render(request, 'contact.html')