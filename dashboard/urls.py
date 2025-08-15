# dashboard/urls.py

from django.urls import path
from .views import  index, health_check

urlpatterns = [
    path('', index, name='dashboard'),
    path('health/', health_check, name='health_check'),
]