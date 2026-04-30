"""
Formulaires Django pour l'application
Auteur: Hamza Marzaq
"""

from django import forms


class PredictionForm(forms.Form):
    """Formulaire de prédiction de culture"""
    
    city = forms.CharField(
        max_length=100,
        required=False,
        label="Ville (optionnel)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Rabat, Casablanca, Marrakech...',
            'id': 'city-input'
        }),
        help_text="Entrez une ville pour récupérer automatiquement la météo"
    )
    
    N = forms.FloatField(
        min_value=0,
        max_value=100,
        label="Azote (N)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0-100',
            'step': '0.1',
            'required': True
        }),
        help_text="Quantité d'azote dans le sol (ratio 0-100)"
    )
    
    P = forms.FloatField(
        min_value=0,
        max_value=100,
        label="Phosphore (P)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0-100',
            'step': '0.1',
            'required': True
        }),
        help_text="Quantité de phosphore dans le sol (ratio 0-100)"
    )
    
    K = forms.FloatField(
        min_value=0,
        max_value=100,
        label="Potassium (K)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0-100',
            'step': '0.1',
            'required': True
        }),
        help_text="Quantité de potassium dans le sol (ratio 0-100)"
    )
    
    temperature = forms.FloatField(
        min_value=-10,
        max_value=50,
        label="Température (°C)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '-10 à 50°C',
            'step': '0.1',
            'required': True,
            'id': 'temperature-input'
        }),
        help_text="Température moyenne en degrés Celsius"
    )
    
    humidity = forms.FloatField(
        min_value=0,
        max_value=100,
        label="Humidité (%)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0-100%',
            'step': '0.1',
            'required': True,
            'id': 'humidity-input'
        }),
        help_text="Humidité relative de l'air (pourcentage)"
    )
    
    ph = forms.FloatField(
        min_value=3,
        max_value=10,
        label="pH du sol",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '3-10',
            'step': '0.1',
            'required': True
        }),
        help_text="Acidité du sol (neutre = 7)"
    )
    
    rainfall = forms.FloatField(
        min_value=0,
        max_value=500,
        label="Précipitations annuelles (mm)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0-500 mm',
            'step': '0.1',
            'required': True
        }),
        help_text="Précipitations annuelles en millimètres"
    )
