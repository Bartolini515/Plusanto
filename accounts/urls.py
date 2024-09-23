from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'), # Przekierowanie na stronę rejestracji
    path('login/', views.signin, name='login'), # Przekierowanie na stronę logowania
]