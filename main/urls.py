from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Przekierowanie na stronę główną w przypadku wejścia na stronę
    path('dashboard/', views.dashboard, name='dashboard'), # Przekierowanie na pulpit
    path('dashboard/informations/', views.informations, name='informations'), # Przekierowanie na informacje użytkownika
    path('about/', views.about, name='about'), # Przekierowanie na pulpit
    path('contact/', views.contact, name='contact') # Przekierowanie na pulpit
]