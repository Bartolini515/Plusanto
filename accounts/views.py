from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, SignInForm

def register(request): # Funkcja rejestracji użytkownika
    if request.method == 'POST': # Sprawdzamy czy użytkownik przesyła dane
        form = RegistrationForm(request.POST)
        if form.is_valid():  # Sprawdzamy czy formularz jest poprawny zgodnie z walidacją
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try: # Sprawdzamy czy użytkownik znajduje się w bazie danych
                existing_user = User.objects.get(username=username)
                if existing_user:
                    messages.info(request, 'Użytkownik o podanej nazwie już istnieje')
                    return render(request, 'register.html', {'form': RegistrationForm(request.POST)})
            except User.DoesNotExist: # Jeżeli użytkownik nie istnieje w bazie danych możemy przejść dalej
                pass
            
            try: # Sprawdzamy czy adres email istnieje w bazie danych
                existing_email = User.objects.get(email=email)
                if existing_email: # Jeżeli email istnieje w bazie danych powracamy do formularza
                    messages.info(request, 'Podany adres email został już powiązany z innym użytkownikiem')
                    return render(request, 'register.html', {'form': RegistrationForm(request.POST)})
            except  User.DoesNotExist: # Jeżeli email nie istnieje w bazie danych możemy przejść dalej
                pass
            
            User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password) # Tworzymy użytkownika w bazie danych
            messages.success(request, "Rejestracja powiodła się!")
            # Logujemy użytkownika
            user = authenticate(request, username=username, password=password) 
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form}) # Jeżeli użytkownik nie wysyła żadnych danych to wyświetli formularz rejestracyjny

def signin(request): # Funkcja logowania  użytkownika
    if request.method == 'POST': # Sprawdzamy czy użytkownik przesyła dane
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)  # Sprawdzamy czy użytkownik istnieje w bazie danych
            if user is not None: #  Jeżeli użytkownik istnieje logujemy go
                login(request, user)
                messages.success(request, "Zalogowano pomyślnie!")
                next_url = request.GET.get('next')
                if next_url: # Jeżeli dostajemy specjalne przekierowanie, to przekierowujemy
                    return redirect(next_url)
                else:
                    return redirect('index')
            else:  # Jeżeli użytkownik nie istnieje wyświetlamy komunikat
                messages.error(request, "Błędne dane logowania!")
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'form': form})

def signout(request): # Funkcja wylogowania użytkownika
    if request.user.is_authenticated: # Tylko jeżeli użytkownik jest zalogowany
        logout(request)
        messages.success(request, "Wylogowano pomyślnie!")
    return redirect('index')