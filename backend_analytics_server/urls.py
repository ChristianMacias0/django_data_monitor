# backend_analytics_server/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

# --- AÑADIMOS ESTAS IMPORTACIONES ---
from dashboard.views import index as dashboard_index
from dashboard.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- RUTA PRINCIPAL EXPLÍCITA ---
    path('', dashboard_index, name='dashboard'),

    # --- RUTA DE SALUD ---
    path('health/', health_check, name='health_check'),

    # --- RUTAS DE AUTENTICACIÓN ---
    path('accounts/login/', auth_views.LoginView.as_view(template_name='security/login.html'), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
]