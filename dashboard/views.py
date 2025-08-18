# dashboard/views.py
import requests
import json
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
        response = requests.get(settings.LANDING_API_URL)
        response.raise_for_status()
        
        products_raw = response.json()

        products = []
        for p in products_raw:
            products.append({
                'product_name': p.get('product_name', 'N/A'),
                'view_count': int(p.get('view_count', 0) / 2)
            })
        
        if products:
            # Los cálculos de los indicadores y la tabla usan la lista completa de productos
            total_products = len(products)
            total_views = sum(p['view_count'] for p in products)
            most_viewed = max(products, key=lambda x: x['view_count'])
            least_viewed = min(products, key=lambda x: x['view_count'])

    except requests.exceptions.RequestException as e:
        error = f"Error al conectar con la API: {e}"
    except (ValueError, KeyError) as e:
        error = f"Error al procesar los datos de la API: {e}"

    # --- NUEVA LÓGICA: PREPARAR DATOS SOLO PARA EL GRÁFICO ---

    # 1. Ordenar la lista de productos de mayor a menor número de vistas
    #    Usamos sorted() para crear una nueva lista ordenada sin modificar la original.
    sorted_products = sorted(products, key=lambda x: x['view_count'], reverse=True)
    
    # 2. Limitar la lista a los primeros 5 productos (los más vistos)
    top_5_products = sorted_products[:5]

    # 3. Preparar las etiquetas y datos para el gráfico a partir de la lista de los 5 mejores
    chart_labels = [p['product_name'] for p in top_5_products]
    chart_data = [p['view_count'] for p in top_5_products]
    
    # Creamos el diccionario de contexto con todos los datos
    context = {
        'title': "Dashboard de Vistas de Productos",
        'products': products, # La tabla usa la lista completa
        'total_products': total_products,
        'total_views': total_views,
        'most_viewed': most_viewed,
        'least_viewed': least_viewed,
        'error': error,
        'chart_labels_json': json.dumps(chart_labels), # Ahora solo contiene los 5 mejores
        'chart_data_json': json.dumps(chart_data),     # Ahora solo contiene sus datos
    }

    return render(request, 'dashboard/index.html', context)