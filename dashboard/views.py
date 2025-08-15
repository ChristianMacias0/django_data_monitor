# dashboard/views.py

# import requests # Temporalmente comentado para depurar el despliegue
import json
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    
    products = []
    total_products = 0
    total_views = 0
    most_viewed = None
    least_viewed = None
    error = None

    try:
        # --- LÓGICA DE API EXTERNA COMENTADA TEMPORALMENTE ---
        # response = requests.get(settings.LANDING_API_URL)
        # response.raise_for_status()
        # products_raw = response.json()
        #
        # products = []
        # for p in products_raw:
        #     products.append({
        #         'product_name': p.get('product_name', 'N/A'),
        #         'view_count': int(p.get('view_count', 0) / 2)
        #     })
        
        # --- DATOS DE EJEMPLO PARA LA PRUEBA DE DESPLIEGUE ---
        products = [
            {'product_name': 'Collares2 (Test)', 'view_count': 24},
            {'product_name': 'Collares1 (Test)', 'view_count': 16},
            {'product_name': 'Collares7 (Test)', 'view_count': 15},
            {'product_name': 'Collares5 (Test)', 'view_count': 9},
            {'product_name': 'Collares6 (Test)', 'view_count': 3},
            {'product_name': 'Pulseras1 (Test)', 'view_count': 3},
        ]
        # ----------------------------------------------------

        if products:
            # Los cálculos de los indicadores y la tabla usan la lista completa de productos
            total_products = len(products)
            total_views = sum(p['view_count'] for p in products)
            most_viewed = max(products, key=lambda x: x['view_count'])
            least_viewed = min(products, key=lambda x: x['view_count'])

    # except requests.exceptions.RequestException as e: # Comentado porque no se usa requests
    #     error = f"Error al conectar con la API: {e}"
    except (ValueError, KeyError) as e:
        # Este error todavía podría ocurrir si los datos de ejemplo estuvieran mal
        error = f"Error al procesar los datos: {e}"

    # --- LÓGICA PARA EL GRÁFICO (sigue funcionando igual) ---
    sorted_products = sorted(products, key=lambda x: x['view_count'], reverse=True)
    top_5_products = sorted_products[:5]
    chart_labels = [p['product_name'] for p in top_5_products]
    chart_data = [p['view_count'] for p in top_5_products]
    
    context = {
        'title': "Dashboard de Vistas de Productos (Modo de Prueba)",
        'products': products,
        'total_products': total_products,
        'total_views': total_views,
        'most_viewed': most_viewed,
        'least_viewed': least_viewed,
        'error': error,
        'chart_labels_json': json.dumps(chart_labels),
        'chart_data_json': json.dumps(chart_data),
    }

    return render(request, 'dashboard/index.html', context)