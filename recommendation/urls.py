"""
URLs de l'application recommendation
Auteur: Hamza Marzaq
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict, name='predict'),
    path('history/', views.history, name='history'),
    path('analytics/', views.analytics, name='analytics'),
    path('api/weather/', views.get_weather, name='get_weather'),
    path('delete/<int:pk>/', views.delete_prediction, name='delete_prediction'),
]
