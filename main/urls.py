from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Przekierowanie na stronę główną w przypadku wejścia na stronę
    path('dashboard/', views.dashboard, name='dashboard'), # Przekierowanie na pulpit
    path('dashboard/budget/', views.budget, name='budget'), # Przekierowanie na budżet
    path('about/', views.about, name='about'), # Przekierowanie na stronę o nas
    path('contact/', views.contact, name='contact'), # Przekierowanie na stronę kontaktową
    path('dashboard/calculator/', views.calculator, name='calculator'), # Przekierowanie na stronę kalkulatora
]