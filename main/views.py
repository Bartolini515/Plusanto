from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

def index(request): # Strona główna
    return render(request, 'index.html')

def dashboard(request): # Pulpit
    if  request.user.is_authenticated:
        return render(request, 'dashboard.html')
    else:
        messages.info(request, "Aby wejść do pulpitu musisz się najpierw zalogować.")
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    
def informations(request): # Informacje o użytkowniku
    return render(request, 'informations.html')