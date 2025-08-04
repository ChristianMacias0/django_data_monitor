# dashboard/views.py

import requests
from django.conf import settings
from django.shortcuts import render

def index(request):
    
    # Realiza la solicitud GET a la URL definida en settings.py
    response = requests.get(settings.API_URL)
    
    # Convierte la respuesta de texto JSON a una lista de diccionarios de Python
    posts = response.json()

    # Calcula el número total de publicaciones recibidas
    total_responses = len(posts)

    # Prepara el contexto para la plantilla
    data = {
        'title': "Dashboard de Analíticas",
        'total_responses': total_responses,
    }

    return render(request, 'dashboard/index.html', data)