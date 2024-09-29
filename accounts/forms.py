from django import forms
from django.core.exceptions import ValidationError


# Formularz z polami: nazwa użytkownika, imię, nazwisko, adres e-mail, hasło i potwierdzenie hasła
class RegistrationForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika')
    first_name = forms.CharField(label='Imię', required=False)
    last_name = forms.CharField(label='Nazwisko', required=False)
    email = forms.EmailField(label='Adres email')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Potwierdź hasło', widget=forms.PasswordInput)
    
    # Formy walidacji danych które przepuszczamy przez formularz
    
    def clean_username(self): # Walidacja długości nazwy użytkownika
        username = self.cleaned_data['username']
        if len(username) < 3:
            raise ValidationError('Nazwa użytkownika musi mieć co najmniej 3 znaki')
        return username

    def clean(self): # Walidacja identyczności haseł
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise ValidationError('Hasła nie są identyczne')
        return cleaned_data