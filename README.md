# 🌾 agriconnect — Application de recommandation agricole

Application web Django qui recommande une culture agricole à partir des paramètres du sol et des conditions météo. Le projet utilise un modèle de Machine Learning entraîné sur un dataset de recommandation de cultures.

## 🎯 Objectif du projet

Aider un utilisateur à saisir des paramètres comme **N, P, K, température, humidité, pH et précipitations**, puis recevoir une recommandation de culture adaptée.

## 👥 Contributeurs

Projet réalisé en binôme dans un cadre académique à l’EMSI.

- Hamza Marzaq
- Hamza Marzaq

**Contribution à personnaliser :** backend Django, intégration du modèle ML, nettoyage des données, interface, sécurité ou tests.

## 🚀 Fonctionnalités

- Recommandation de culture avec un modèle Machine Learning
- Interface web avec Django
- Formulaire de prédiction
- Historique des prédictions
- Page d’analyse avec graphiques
- Intégration météo via OpenWeatherMap
- Validation des entrées utilisateur
- Protection CSRF et bonnes pratiques Django

## 🛠️ Technologies utilisées

- Python
- Django
- Scikit-learn
- Pandas
- NumPy
- MySQL
- HTML / CSS / JavaScript
- Bootstrap
- Chart.js
- Git / GitHub

## 📁 Structure du projet

```txt
agriconnect/
├── agriconnect/                  # Configuration Django
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
```

## ⚙️ Installation locale

### 1. Cloner le projet

```bash
git clone https://github.com/TON-COMPTE/agriconnect.git
cd agriconnect
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
```

Windows :

```bash
venv\Scripts\activate
```

Linux / Mac :

```bash
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Créer le fichier `.env`

Windows :

```bash
copy .env.example .env
```

Linux / Mac :

```bash
cp .env.example .env
```

Ensuite modifier `.env` avec tes informations MySQL et ta clé OpenWeatherMap.

### 5. Créer la base MySQL

```sql
CREATE DATABASE agriconnect CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Appliquer les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Lancer le serveur

```bash
python manage.py runserver
```

Puis ouvrir :

```txt
http://127.0.0.1:8000/
```

## 🔐 Variables d’environnement

Le fichier `.env` ne doit jamais être envoyé sur GitHub. Utiliser `.env.example` comme modèle.

```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
MYSQL_DATABASE=agriconnect
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_HOST=localhost
MYSQL_PORT=3306
OPENWEATHER_API_KEY=your-api-key
```

## 🧪 Commandes utiles

```bash
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py test
```

## 📌 Remarque portfolio

Ce projet montre des compétences en développement web Django, intégration Machine Learning, manipulation de données, base de données relationnelle, structuration GitHub et documentation technique.

## 📄 Licence

Projet académique — usage pédagogique.
