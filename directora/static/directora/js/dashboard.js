document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('proyectosChart').getContext('2d');
    const proyectosChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Pendientes', 'En Progreso', 'Terminados'],
            datasets: [{
                label: 'Número de Proyectos',
                data: JSON.parse(document.getElementById('chartData').value),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(75, 192, 192, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Función para descargar el gráfico como PDF
    window.downloadPDF = function() {
        console.log("Generando PDF...");
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        doc.text("Reporte de Proyectos", 10, 10);
        doc.text("Este documento contiene un resumen gráfico de los estados de los proyectos.", 10, 20);

        // Obtener la imagen base64 del gráfico
        const chartImgData = proyectosChart.toBase64Image();
        console.log("Imagen del gráfico obtenida", chartImgData);

        // Añadir la imagen al PDF
        doc.addImage(chartImgData, 'PNG', 15, 30, 180, 100);

        // Guardar el PDF
        doc.save('reporte_proyectos.pdf');
    };
});
