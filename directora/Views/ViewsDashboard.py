
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
import openpyxl
from openpyxl.chart import BarChart, Reference
from directora.models import Proyecto  # Import the Proyecto model

def obtener_rol(user):
    if user.groups.filter(name='Directora').exists():
        return 'Directora'
    elif user.groups.filter(name='Asistente').exists():
        return 'Asistente'
    elif user.groups.filter(name='Técnica de Campo').exists():
        return 'Técnica de Campo'
    else:
        return 'default'
@login_required
def dashboard_proyectos(request):
    # Obtiene el rol del usuario actual
    rol = obtener_rol(request.user)
    
    # Cuenta los proyectos en diferentes estados
    proyectos_pendientes = Proyecto.objects.filter(estado='pendiente').count()
    proyectos_en_progreso = Proyecto.objects.filter(estado='en_progreso').count()
    proyectos_terminados = Proyecto.objects.filter(estado='completado').count()
    
    # Prepara el contexto para la plantilla
    context = {
        'proyectos_pendientes': proyectos_pendientes,
        'proyectos_en_progreso': proyectos_en_progreso,
        'proyectos_terminados': proyectos_terminados,
        'rol': rol
    }
    
    # Renderiza la plantilla 'dashboard_proyectos.html' con el contexto
    return render(request, 'directora/DashboardDirectora/dashboard_proyectos.html', context)


@login_required
def exportar_proyectos_excel(request):
    # Crear un libro de Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Proyectos'

    # Agregar los encabezados
    ws.append(['Estado', 'Número de Proyectos'])

    # Obtener los datos del gráfico
    proyectos_pendientes = Proyecto.objects.filter(estado='pendiente').count()
    proyectos_en_progreso = Proyecto.objects.filter(estado='en_progreso').count()
    proyectos_terminados = Proyecto.objects.filter(estado='completado').count()

    # Agregar los datos al archivo Excel
    ws.append(['Pendientes', proyectos_pendientes])
    ws.append(['En Progreso', proyectos_en_progreso])
    ws.append(['Completados', proyectos_terminados])

    # Crear la respuesta HTTP para enviar el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=proyectos.xlsx'

    # Guardar el archivo Excel en la respuesta
    wb.save(response)
    return response


@login_required
def exportar_proyectos_excel_con_grafico(request):
    # Obtener el rol del usuario actual
    rol = obtener_rol(request.user)

    # Crear un nuevo libro de Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Proyectos'

    # Agregar los encabezados a la hoja de cálculo
    ws.append(['Estado', 'Pendientes', 'En Progreso', 'Completados'])

    # Obtener los datos del gráfico
    proyectos_pendientes = Proyecto.objects.filter(estado='pendiente').count()
    proyectos_en_progreso = Proyecto.objects.filter(estado='en_progreso').count()
    proyectos_terminados = Proyecto.objects.filter(estado='completado').count()

    # Agregar los datos al archivo Excel (cada estado es una serie)
    ws.append(['Proyectos', proyectos_pendientes, proyectos_en_progreso, proyectos_terminados])

    # Crear un gráfico de barras
    chart = BarChart()
    chart.title = "Proyectos por Estado"
    chart.x_axis.title = "Estado"
    chart.y_axis.title = "Número de Proyectos"

    # Definir el rango de datos para el gráfico
    data = Reference(ws, min_col=2, min_row=1, max_row=2, max_col=4)  # Cada columna es una serie
    categories = Reference(ws, min_col=1, min_row=2, max_row=2)  # Categoría (nombre de los estados)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(categories)

    # Definir colores personalizados para cada serie (estado)
    colors = ["FF0000", "0000FF", "00FF00"]  # Rojo, Azul, Verde
    for i, serie in enumerate(chart.series):
        serie.graphicalProperties.solidFill = colors[i]

    # Insertar el gráfico en la hoja de cálculo
    ws.add_chart(chart, "E5")

    # Crear la respuesta HTTP para enviar el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="proyectos_con_grafico.xlsx"'

    # Guardar el archivo Excel en la respuesta
    wb.save(response)
    return response