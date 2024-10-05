from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


# Formularz z polami: nazwa użytkownika, imię, nazwisko, adres e-mail, hasło i potwierdzenie hasła
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
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError(e.messages[0])
        return password

    def clean_confirm(self): # Walidacja identyczności haseł # TODO : nie działa sprawdzanie hasła oraz wywala baze danych jeżeli są znaki polskie
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise ValidationError('Hasła nie są identyczne')
        return cleaned_data