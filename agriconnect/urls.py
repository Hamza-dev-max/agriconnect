"""
URL configuration for agriconnect project.
Application de Recommandation Agricole v3.0 - Django Web App
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recommendation.urls')),
]

# Servir les fichiers statiques et médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Personnalisation de l'admin
admin.site.site_header = "🌾 Administration Agricole"
admin.site.site_title = "agriconnect Admin"
admin.site.index_title = "Gestion de l'application"
