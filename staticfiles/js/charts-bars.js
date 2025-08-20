/**
 * For usage, visit Chart.js docs https://www.chartjs.org/docs/latest/
 */
const barConfig = {
  type: 'bar',
  data: {
    // <<< CAMBIO CLAVE: Las etiquetas ahora vienen de la variable de Django
    labels: chartLabels, 
    datasets: [
      {
        // <<< CAMBIO CLAVE: Solo un dataset para los productos
        label: 'Vistas por Producto (Dividido)',
        backgroundColor: '#7e3af2', // Color púrpura para las barras
        borderColor: '#7e3af2',
        // <<< CAMBIO CLAVE: Los datos ahora vienen de la variable de Django
        data: chartData,
        borderWidth: 1,
      },
      // <<< CAMBIO CLAVE: Eliminamos el segundo dataset de ejemplo que estaba aquí
    ],
  },
  options: {
    responsive: true,
    legend: {
      display: false, // Ocultamos la leyenda ya que solo hay una serie de datos
    },
    tooltips: {
      mode: 'index',
      intersect: false,
    },
    hover: {
      mode: 'nearest',
      intersect: true,
    },
    scales: {
      x: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Producto', // Etiqueta para el eje X
        },
      },
      y: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Número de Vistas', // Etiqueta para el eje Y
        },
        // Hacemos que la escala empiece en 0
        ticks: {
            beginAtZero: true,
        },
      },
    },
  },
}

// Inicializa el gráfico
const barsCtx = document.getElementById('bars')
if (barsCtx) {
  window.myBar = new Chart(barsCtx, barConfig)
}