# backend_analytics_server/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # Importamos las vistas de autenticación
from dashboard.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),

    # --- CONFIGURACIÓN DE AUTENTICACIÓN EXPLÍCITA ---
    
    # 1. Vista de Login:
    # Le decimos a Django que use su LoginView, pero que la renderice
    # con NUESTRA plantilla específica en 'security/login.html'.
    path(
        'accounts/login/', 
        auth_views.LoginView.as_view(template_name='security/login.html'), 
        name='login'
    ),
    
    # 2. Vista de Logout:
    # Le decimos a Django que use su LogoutView.
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # --- RUTA PRINCIPAL ---
    # Esta debe ir al final para no capturar las rutas de 'accounts/'.
    path('', include('dashboard.urls')),
]