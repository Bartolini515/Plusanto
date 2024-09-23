from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Przekierowanie na stronę główną w przypadku wejścia na stronę
    path('home/', views.index, name='home'),  # Przekierowanie na stronę główną w przypadku wyjścia z innej funkcji
]