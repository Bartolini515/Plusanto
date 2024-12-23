from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


# Formularz dla rejestracji
class RegistrationForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika', max_length=60, widget=forms.TextInput(attrs={'placeholder': 'Wprowadź nazwę użytkownika'}))
    first_name = forms.CharField(label='Imię', required=False, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Wprowadź swoje imię'}))
    last_name = forms.CharField(label='Nazwisko', required=False, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Wprowadź swoje nazwisko'}))
    email = forms.EmailField(label='Adres email', max_length=60, widget=forms.EmailInput(attrs={'placeholder': 'Wprowadź swój adres e-mail'}))
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'placeholder': 'Wprowadź hasło'}))
    password_confirm = forms.CharField(label='Potwierdź hasło', widget=forms.PasswordInput(attrs={'placeholder': 'Wprowadź ponownie hasło'}))
    
    # Formy walidacji danych które przepuszczamy przez formularz
    
    def clean_username(self): # Walidacja długości nazwy użytkownika
        username = self.cleaned_data['username']
        if len(username) < 3:
            raise ValidationError('Nazwa użytkownika musi mieć co najmniej 3 znaki')
        return username
    
    def clean_password(self): # Walidacja hasła poprzez wbudowane moduły django
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError(e.messages[0])
        return password

    def clean_password_confirm(self): # Walidacja identyczności haseł
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise ValidationError('Hasła nie są identyczne')
        return password, password_confirm


# Formularz dla logowania
class SignInForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika', max_length=60, widget=forms.TextInput(attrs={'placeholder': 'Wprowadź nazwę użytkownika'}))
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'placeholder': 'Wprowadź hasło'}))