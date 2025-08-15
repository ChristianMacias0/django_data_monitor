# backend_analytics_server/urls.py

from django.contrib import admin
from django.urls import path, include
from dashboard.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),

    # --- CAMBIO IMPORTANTE: Usamos include para las URLs de autenticación ---
    # Esto es más robusto. Django buscará 'accounts/login/', 'accounts/logout/', etc.
    path('accounts/', include('django.contrib.auth.urls')),
    
    # --- CAMBIO IMPORTANTE: Incluimos la app del dashboard ---
    # La ruta raíz ahora es manejada por dashboard.urls
    path('', include('dashboard.urls')),
]