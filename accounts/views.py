from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm

def register(request): # Funkcja rejestracji użytkownika
    if request.method == 'POST': # Sprawdzamy czy użytkownik przesyła dane
        form = RegistrationForm(request.POST)
        if form.is_valid():  # Sprawdzamy czy formularz jest poprawny zgodnie z walidacją
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, email=email)
            if user is not None: # Jeżeli użytkownik istnieje powracamy do formularza
                messages.info(request, 'Użytkownik o podanej nazwie i email już istnieje')
                form = UserCreationForm()
                return render(request, 'register.html', {'form': form})
            User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password) # Tworzymy użytkownika w bazie danych
            messages.success(request, "Rejestracja powiodła się!")
            # Logujemy użytkownika
            user = authenticate(request, username=username, password=password) 
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form}) # Jeżeli użytkownik nie wysyła żadnych danych to wyświetli formularz rejestracyjny

def signin(request): # Funckja logowania  użytkownika
    if request.method == 'POST': # Sprawdzamy czy użytkownik przesyła dane
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)  # Sprawdzamy czy użytkownik istnieje w bazie danych
        if user is not None: #  Jeżeli użytkownik istnieje logujemy go
            login(request, user)
            messages.success(request, "Zalogowano pomyślnie!")
            return redirect('home')
        else:  # Jeżeli użytkownik nie istnieje wyświetlamy komunikat
            messages.error(request, "Błędne dane logowania!")
    return render(request, 'signin.html')