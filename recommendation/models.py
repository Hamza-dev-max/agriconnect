"""
Modèles Django pour l'application de recommandation agricole
Auteur: Hamza Marzaq
"""

from django.db import models
from django.utils import timezone


class CropData(models.Model):
    """
    Données d'entraînement pour le modèle ML
    Table existante: crop_recommendation
    """
    N = models.FloatField(verbose_name="Azote (N)")
    P = models.FloatField(verbose_name="Phosphore (P)")
    K = models.FloatField(verbose_name="Potassium (K)")
    temperature = models.FloatField(verbose_name="Température (°C)")
    humidity = models.FloatField(verbose_name="Humidité (%)")
    ph = models.FloatField(verbose_name="pH du sol")
    rainfall = models.FloatField(verbose_name="Précipitations (mm)")
    label = models.CharField(max_length=50, verbose_name="Culture")
    
    class Meta:
        db_table = 'crop_recommendation'
        managed = False  # Ne pas gérer cette table (elle existe déjà)
        verbose_name = "Donnée de culture"
        verbose_name_plural = "Données de cultures"
    
    def __str__(self):
        return f"{self.label} - N:{self.N} P:{self.P} K:{self.K}"


class Prediction(models.Model):
    """Historique des prédictions"""
    city = models.CharField(max_length=100, verbose_name="Ville", blank=True)
    predicted_crop = models.CharField(max_length=50, verbose_name="Culture prédite")
    N = models.FloatField(verbose_name="Azote (N)")
    P = models.FloatField(verbose_name="Phosphore (P)")
    K = models.FloatField(verbose_name="Potassium (K)")
    temperature = models.FloatField(verbose_name="Température (°C)")
    humidity = models.FloatField(verbose_name="Humidité (%)")
    ph = models.FloatField(verbose_name="pH du sol")
    rainfall = models.FloatField(verbose_name="Précipitations (mm)")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de prédiction")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Prédiction"
        verbose_name_plural = "Prédictions"
    
    def __str__(self):
        return f"{self.city or 'Non spécifiée'} - {self.predicted_crop} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
    
    def get_parameters_dict(self):
        """Retourne les paramètres sous forme de dictionnaire"""
        return {
            'N': self.N,
            'P': self.P,
            'K': self.K,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'ph': self.ph,
            'rainfall': self.rainfall
        }
