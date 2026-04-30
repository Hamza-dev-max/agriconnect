"""
Configuration de l'admin Django
Auteur: Hamza Marzaq
"""

from django.contrib import admin
from .models import Prediction, CropData


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    """Administration des prédictions"""
    list_display = ('city', 'predicted_crop', 'created_at', 'N', 'P', 'K', 'temperature')
    list_filter = ('predicted_crop', 'created_at')
    search_fields = ('city', 'predicted_crop')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('city', 'predicted_crop', 'created_at')
        }),
        ('Paramètres du sol', {
            'fields': ('N', 'P', 'K', 'ph')
        }),
        ('Conditions météorologiques', {
            'fields': ('temperature', 'humidity', 'rainfall')
        }),
    )
    
    readonly_fields = ('created_at',)


@admin.register(CropData)
class CropDataAdmin(admin.ModelAdmin):
    """Administration des données de cultures"""
    list_display = ('label', 'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall')
    list_filter = ('label',)
    search_fields = ('label',)
    ordering = ('label',)
