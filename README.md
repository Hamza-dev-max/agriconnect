# 🌾 AgriConnect — Application de recommandation agricole

AgriConnect est une application web développée avec Django qui recommande une culture agricole à partir des paramètres du sol et des conditions climatiques. Le projet utilise un modèle de Machine Learning entraîné sur un dataset de recommandation de cultures.

## 🎯 Objectif du projet

L’objectif est d’aider l’utilisateur à saisir des paramètres agricoles comme **N, P, K, température, humidité, pH et précipitations**, puis recevoir une recommandation de culture adaptée.

## 👤 Auteur

Projet réalisé dans un cadre académique à l’EMSI.

- Hamza Marzaq

## 💼 Contribution

Dans ce projet, j’ai travaillé sur la structuration de l’application Django, l’intégration du modèle de Machine Learning, la gestion du formulaire de prédiction, l’historique des résultats, la page d’analyse des données, l’intégration météo via API et la préparation du projet pour GitHub.

## 🚀 Fonctionnalités

- Recommandation de culture avec un modèle de Machine Learning
- Interface web avec Django
- Formulaire de prédiction
- Historique des prédictions
- Page d’analyse avec graphiques
- Lecture du dataset `Crop_recommendation.csv`
- Intégration météo via OpenWeatherMap
- Validation des entrées utilisateur
- Protection CSRF et bonnes pratiques Django

## 🛠️ Technologies utilisées

- Python
- Django
- Scikit-learn
- Pandas
- NumPy
- SQLite / MySQL
- HTML / CSS / JavaScript
- Bootstrap
- Chart.js
- Git / GitHub

## 📁 Structure du projet

```txt
agriconnect/
├── agriconnect/              # Configuration Django
├── recommendation/           # Application principale
│   ├── templates/            # Pages HTML
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── ml_utils.py
├── Crop_recommendation.csv   # Dataset
├── model.pkl                 # Modèle ML entraîné
├── manage.py
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
