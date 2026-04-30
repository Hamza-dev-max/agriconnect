"""
Vues Django pour l'application AgriConnect
Auteur: Hamza Marzaq
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
import requests
import csv

from .models import Prediction
from .forms import PredictionForm
from .ml_utils import get_predictor


def home(request):
    """Page d'accueil"""
    total_predictions = Prediction.objects.count()
    recent_predictions = Prediction.objects.all()[:5]

    context = {
        'total_predictions': total_predictions,
        'recent_predictions': recent_predictions,
    }
    return render(request, 'home.html', context)


def predict(request):
    """Page de prédiction"""
    import logging
    logger = logging.getLogger('django.security')

    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data.get('city', '').strip()

            try:
                features = {
                    'N': float(form.cleaned_data['N']),
                    'P': float(form.cleaned_data['P']),
                    'K': float(form.cleaned_data['K']),
                    'temperature': float(form.cleaned_data['temperature']),
                    'humidity': float(form.cleaned_data['humidity']),
                    'ph': float(form.cleaned_data['ph']),
                    'rainfall': float(form.cleaned_data['rainfall']),
                }

                if not (0 <= features['N'] <= 100):
                    raise ValueError("N doit être entre 0 et 100")
                if not (0 <= features['P'] <= 100):
                    raise ValueError("P doit être entre 0 et 100")
                if not (0 <= features['K'] <= 100):
                    raise ValueError("K doit être entre 0 et 100")
                if not (0 <= features['temperature'] <= 50):
                    raise ValueError("Température doit être entre 0 et 50°C")
                if not (0 <= features['humidity'] <= 100):
                    raise ValueError("Humidité doit être entre 0 et 100%")
                if not (3 <= features['ph'] <= 10):
                    raise ValueError("pH doit être entre 3 et 10")
                if not (0 <= features['rainfall'] <= 500):
                    raise ValueError("Précipitations doivent être entre 0 et 500mm")

            except (ValueError, TypeError) as e:
                logger.warning(f"Tentative de soumission avec des valeurs invalides: {e}")
                messages.error(request, f'❌ Valeurs invalides : {str(e)}')
                return render(request, 'predict.html', {'form': form})

            try:
                predictor = get_predictor()
                predicted_crop = predictor.predict(features)

                from django.utils.html import escape
                safe_city = escape(city) if city else "Non spécifiée"

                Prediction.objects.create(
                    city=safe_city,
                    predicted_crop=predicted_crop,
                    **features
                )

                logger.info(f"Prédiction réussie: {predicted_crop} pour {safe_city}")

                messages.success(
                    request,
                    f'🌱 Culture recommandée : <strong>{escape(predicted_crop)}</strong>'
                )

                return redirect('history')

            except Exception as e:
                logger.error(f"Erreur lors de la prédiction: {str(e)}")
                messages.error(
                    request,
                    '❌ Erreur lors de la prédiction : Une erreur technique est survenue.'
                )
        else:
            logger.warning(f"Formulaire invalide: {form.errors}")
    else:
        form = PredictionForm()

    return render(request, 'predict.html', {'form': form})


def history(request):
    """Page d'historique des prédictions"""
    predictions = Prediction.objects.all()

    from django.db.models import Count
    top_crops = predictions.values('predicted_crop').annotate(
        count=Count('predicted_crop')
    ).order_by('-count')[:5]

    context = {
        'predictions': predictions,
        'total': predictions.count(),
        'top_crops': top_crops,
    }
    return render(request, 'history.html', context)


def get_weather(request):
    """API pour récupérer la météo AJAX"""
    import logging
    import re
    logger = logging.getLogger('django.security')

    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        logger.warning(f"Tentative d'accès direct à l'API météo depuis {request.META.get('REMOTE_ADDR')}")
        return JsonResponse({'error': 'Requête non autorisée'}, status=403)

    city = request.GET.get('city', '').strip()

    if not city:
        return JsonResponse({'error': 'Ville non spécifiée'}, status=400)

    if not re.match(r'^[a-zA-ZÀ-ÿ\s\-]{2,50}$', city):
        logger.warning(f"Tentative d'injection dans le nom de ville: {city}")
        return JsonResponse({
            'error': 'Nom de ville invalide. Utilisez uniquement des lettres.'
        }, status=400)

    api_key = settings.OPENWEATHER_API_KEY
    if not api_key or api_key == "your-openweathermap-api-key":
        logger.error("Clé API OpenWeatherMap non configurée")
        return JsonResponse({
            'error': 'Clé API météo non configurée'
        }, status=500)

    from urllib.parse import quote
    safe_city = quote(city)

    url = f"https://api.openweathermap.org/data/2.5/weather?q={safe_city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return JsonResponse({
                'error': data.get('message', 'Ville introuvable ou clé API invalide')
            }, status=response.status_code)

        weather_data = {
            'temperature': round(float(data["main"]["temp"]), 1),
            'humidity': int(data["main"]["humidity"]),
            'city': str(data["name"])[:50],
            'country': str(data["sys"]["country"])[:2],
        }

        return JsonResponse(weather_data)

    except requests.exceptions.Timeout:
        return JsonResponse({'error': 'Délai d’attente dépassé'}, status=408)
    except requests.exceptions.ConnectionError:
        return JsonResponse({'error': 'Impossible de se connecter au service météo'}, status=503)
    except Exception as e:
        logger.error(f"Erreur météo: {str(e)}")
        return JsonResponse({'error': 'Une erreur technique est survenue'}, status=500)


def delete_prediction(request, pk):
    """Supprimer une prédiction"""
    if request.method == 'POST':
        try:
            prediction = Prediction.objects.get(pk=pk)
            prediction.delete()
            messages.success(request, '✅ Prédiction supprimée')
        except Prediction.DoesNotExist:
            messages.error(request, '❌ Prédiction introuvable')

    return redirect('history')


def load_crop_csv():
    """Lire le dataset depuis Crop_recommendation.csv"""
    csv_path = settings.BASE_DIR / "Crop_recommendation.csv"
    crop_rows = []

    try:
        with open(csv_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            for row in reader:
                crop_rows.append({
                    "N": float(row["N"]),
                    "P": float(row["P"]),
                    "K": float(row["K"]),
                    "temperature": float(row["temperature"]),
                    "humidity": float(row["humidity"]),
                    "ph": float(row["ph"]),
                    "rainfall": float(row["rainfall"]),
                    "label": row["label"],
                })

        print("Nombre de lignes CSV chargées:", len(crop_rows))

    except Exception as e:
        print("Erreur lecture CSV:", e)
        crop_rows = []

    return crop_rows


def analytics(request):
    """Page d'analyse de données avec graphiques depuis le CSV"""
    from django.db.models import Count
    import json
    from collections import defaultdict

    predictions = Prediction.objects.all()
    crop_rows = load_crop_csv()

    total_predictions = predictions.count()
    total_crops = len(crop_rows)

    crop_distribution = list(
        predictions.values("predicted_crop")
        .annotate(count=Count("predicted_crop"))
        .order_by("-count")
    )

    dataset_count = defaultdict(int)
    for row in crop_rows:
        dataset_count[row["label"]] += 1

    dataset_distribution = [
        {"label": label, "count": count}
        for label, count in sorted(dataset_count.items(), key=lambda x: x[1], reverse=True)
    ]

    sums = defaultdict(lambda: {
        "count": 0,
        "N": 0,
        "P": 0,
        "K": 0,
        "temperature": 0,
        "humidity": 0,
        "ph": 0,
        "rainfall": 0,
    })

    for row in crop_rows:
        label = row["label"]
        sums[label]["count"] += 1
        sums[label]["N"] += row["N"]
        sums[label]["P"] += row["P"]
        sums[label]["K"] += row["K"]
        sums[label]["temperature"] += row["temperature"]
        sums[label]["humidity"] += row["humidity"]
        sums[label]["ph"] += row["ph"]
        sums[label]["rainfall"] += row["rainfall"]

    crop_averages = []
    for label, values in sorted(sums.items()):
        count = values["count"]
        crop_averages.append({
            "label": label,
            "avg_N": values["N"] / count,
            "avg_P": values["P"] / count,
            "avg_K": values["K"] / count,
            "avg_temp": values["temperature"] / count,
            "avg_humidity": values["humidity"] / count,
            "avg_ph": values["ph"] / count,
            "avg_rainfall": values["rainfall"] / count,
        })

    predictions_by_month_dict = defaultdict(int)
    for pred in predictions:
        month_key = pred.created_at.strftime("%B %Y")
        predictions_by_month_dict[month_key] += 1

    predictions_by_month = [
        {"month": month, "count": count}
        for month, count in sorted(predictions_by_month_dict.items())
    ]

    top_cities = list(
        predictions.exclude(city="Non spécifiée")
        .values("city")
        .annotate(count=Count("city"))
        .order_by("-count")[:10]
    )

    def get_stats(field):
        values = [row[field] for row in crop_rows]
        if not values:
            return {"min": 0, "max": 0, "avg": 0}
        return {
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
        }

    param_stats = {
        "N": get_stats("N"),
        "P": get_stats("P"),
        "K": get_stats("K"),
        "temperature": get_stats("temperature"),
        "humidity": get_stats("humidity"),
        "ph": get_stats("ph"),
        "rainfall": get_stats("rainfall"),
    }

    chart_data = {
        "crop_distribution": {
            "labels": [item["predicted_crop"] for item in crop_distribution],
            "data": [item["count"] for item in crop_distribution],
        },
        "dataset_distribution": {
            "labels": [item["label"] for item in dataset_distribution],
            "data": [item["count"] for item in dataset_distribution],
        },
        "predictions_by_month": {
            "labels": [item["month"] for item in predictions_by_month],
            "data": [item["count"] for item in predictions_by_month],
        },
        "top_cities": {
            "labels": [item["city"] for item in top_cities],
            "data": [item["count"] for item in top_cities],
        },
        "crop_averages": {
            "labels": [item["label"] for item in crop_averages],
            "N": [round(item["avg_N"], 2) for item in crop_averages],
            "P": [round(item["avg_P"], 2) for item in crop_averages],
            "K": [round(item["avg_K"], 2) for item in crop_averages],
        },
    }

    context = {
        "total_predictions": total_predictions,
        "total_crops": total_crops,
        "crop_distribution": crop_distribution,
        "dataset_distribution": dataset_distribution,
        "top_cities": top_cities,
        "param_stats": param_stats,
        "chart_data_json": json.dumps(chart_data),
    }

    return render(request, "analytics.html", context)