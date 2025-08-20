# dashboard/views.py
import requests
import json
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings 
from django.shortcuts import render 
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('dashboard.index_viewer', raise_exception=True)

def index(request):
    
    products = []
    total_products = 0
    total_views = 0
    most_viewed = None
    least_viewed = None
    error = None

    try:
        # Hacemos la solicitud con un timeout para evitar que se quede colgada
        response = requests.get(settings.LANDING_API_URL, timeout=10) # 10 segundos de espera
        response.raise_for_status() # Lanza un error si el código no es 2xx
        
        products_raw = response.json()

        products = []
        for p in products_raw:
            products.append({
                'product_name': p.get('product_name', 'N/A'),
                'view_count': int(p.get('view_count', 0)) # No dividimos aquí para simplificar
            })
        
        if products:
            total_products = len(products)
            total_views = sum(p['view_count'] for p in products)
            most_viewed = max(products, key=lambda x: x['view_count'])
            least_viewed = min(products, key=lambda x: x['view_count'])

    except requests.exceptions.RequestException as e:
        # Si la API no responde o hay un error de red, lo capturamos y lo mostramos
        error = f"No se pudo conectar con la API de productos en {settings.LANDING_API_URL}. Detalles: {e}"
    except (ValueError, KeyError) as e:
        # Si el JSON está mal formado o faltan claves
        error = f"Error al procesar los datos de la API. Detalles: {e}"

    # Lógica del gráfico (ahora es segura incluso si 'products' está vacía)
    sorted_products = sorted(products, key=lambda x: x['view_count'], reverse=True)
    top_5_products = sorted_products[:5]
    chart_labels = [p['product_name'] for p in top_5_products]
    chart_data = [p['view_count'] for p in top_5_products]
    
    context = {
        'title': "Dashboard de Vistas de Productos",
        'products': products,
        'total_products': total_products,
        'total_views': total_views,
        'most_viewed': most_viewed,
        'least_viewed': least_viewed,
        'error': error, # Pasamos el mensaje de error a la plantilla
        'chart_labels_json': json.dumps(chart_labels),
        'chart_data_json': json.dumps(chart_data),
    }

    return render(request, 'dashboard/index.html', context)


# Vista de Health Check
def health_check(request):
    return HttpResponse("OK", status=200)