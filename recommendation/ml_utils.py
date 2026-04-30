"""
Utilitaires Machine Learning
Auteur: Hamza Marzaq
"""

import pickle
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from django.conf import settings


# Traductions des cultures
CROP_TRANSLATIONS = {
    "rice": "Riz",
    "maize": "Maïs",
    "chickpea": "Pois chiche",
    "kidneybeans": "Haricot rouge",
    "pigeonpeas": "Pois d'Angole",
    "mothbeans": "Haricot papillon",
    "mungbean": "Haricot mungo",
    "blackgram": "Haricot urd",
    "lentil": "Lentille",
    "pomegranate": "Grenade",
    "banana": "Banane",
    "mango": "Mangue",
    "grapes": "Raisin",
    "watermelon": "Pastèque",
    "muskmelon": "Melon",
    "apple": "Pomme",
    "orange": "Orange",
    "papaya": "Papaye",
    "coconut": "Noix de coco",
    "cotton": "Coton",
    "jute": "Jute",
    "coffee": "Café"
}


class MLPredictor:
    """Classe pour gérer les prédictions ML"""
    
    def __init__(self):
        self.model = None
        self.model_path = settings.ML_MODEL_PATH
        self.load_model()
    
    def load_model(self):
        """Charge le modèle depuis le fichier pickle"""
        try:
            if Path(self.model_path).exists():
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print(f"✅ Modèle chargé depuis {self.model_path}")
            else:
                print(f"⚠️ Modèle non trouvé, entraînement nécessaire")
                self.train_model()
        except Exception as e:
            print(f"⚠️ Erreur lors du chargement : {e}")
            self.train_model()
    
    def train_model(self):
        """Entraîne un nouveau modèle"""
        from .models import CropData
        
        print("🤖 Entraînement du modèle...")
        
        # Récupérer les données
        data = CropData.objects.all().values()
        df = pd.DataFrame(data)
        
        if len(df) == 0:
            raise ValueError("Aucune donnée d'entraînement disponible")
        
        # Séparation features/labels
        X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
        y = df['label']
        
        # Split train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Entraînement
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=20,
            min_samples_split=5
        )
        self.model.fit(X_train, y_train)
        
        # Évaluation
        accuracy = self.model.score(X_test, y_test)
        print(f"✅ Modèle entraîné - Précision: {accuracy:.2%}")
        
        # Sauvegarde
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"💾 Modèle sauvegardé dans {self.model_path}")
    
    def predict(self, features_dict):
        """
        Fait une prédiction
        
        Args:
            features_dict (dict): Dictionnaire avec N, P, K, temperature, humidity, ph, rainfall
        
        Returns:
            str: Culture prédite (en français)
        """
        if self.model is None:
            raise ValueError("Modèle non chargé")
        
        # Créer DataFrame
        features_df = pd.DataFrame([features_dict])
        
        # Prédiction
        prediction = self.model.predict(features_df)[0]
        
        # Traduction
        prediction_fr = CROP_TRANSLATIONS.get(prediction, prediction)
        
        return prediction_fr


# Instance globale du prédicteur
_predictor = None

def get_predictor():
    """Retourne l'instance du prédicteur (singleton)"""
    global _predictor
    if _predictor is None:
        _predictor = MLPredictor()
    return _predictor
