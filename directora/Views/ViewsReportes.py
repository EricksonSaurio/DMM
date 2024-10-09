from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Proyecto, Tarea, Empleado, PerfilUsuario
from django.http import HttpResponse
from xhtml2pdf import pisa
import pandas as pd
from django.template.loader import render_to_string
import plotly.graph_objs as go
from plotly.offline import plot
from django.utils import timezone
from datetime import datetime
from collections import Counter

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
def reporte_proyectos(request):
    # Obtiene el rol del usuario actual
    rol = obtener_rol(request.user)

    # Filtros para tareas
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    empleado_id = request.GET.get('empleado')

    empleados = Empleado.objects.all()
    proyectos = Proyecto.objects.all()
    tareas = Tarea.objects.all()

    # Variable para almacenar el empleado con más tareas
    empleado_mas_tareas = None
    tareas_empleado_mas_tareas = 0

    # Aplicar filtros a las tareas si hay fechas proporcionadas
    if fecha_inicio and fecha_fin:
        try:
            # Convertir las fechas a aware con zona horaria
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
            fecha_inicio_aware = timezone.make_aware(fecha_inicio_dt)
            fecha_fin_aware = timezone.make_aware(fecha_fin_dt)

            # Filtrar tareas por empleado y fechas
            if empleado_id and empleado_id != "":
                perfil_usuario = PerfilUsuario.objects.filter(empleado_id=empleado_id).first()
                if perfil_usuario:
                    tareas = tareas.filter(
                        asignada_a=perfil_usuario.user, 
                        fecha_creacion__range=[fecha_inicio_aware, fecha_fin_aware]
                    )
                else:
                    tareas = Tarea.objects.none()
            else:
                tareas = tareas.filter(
                    fecha_creacion__range=[fecha_inicio_aware, fecha_fin_aware]
                )
        except Exception as e:
            print(f"Error al filtrar tareas: {e}")

    else:
        # Si no hay filtros aplicados, determinar el empleado con más tareas
        tareas_por_empleado = Counter(tarea.asignada_a.id for tarea in tareas)
        print(f"Conteo de tareas por empleado: {tareas_por_empleado}")  # Depuración: verificar conteo

        if tareas_por_empleado:
            empleado_id_con_mas_tareas = max(tareas_por_empleado, key=tareas_por_empleado.get)
            tareas_empleado_mas_tareas = tareas_por_empleado[empleado_id_con_mas_tareas]

            try:
                # Intentar obtener el empleado relacionado con el perfil de usuario
                empleado_mas_tareas = Empleado.objects.filter(perfilusuario__user__id=empleado_id_con_mas_tareas).first()
                print(f"Empleado con más tareas: {empleado_mas_tareas}, Tareas: {tareas_empleado_mas_tareas}")
            except Exception as e:
                print(f"Error al obtener el empleado con más tareas: {e}")
                empleado_mas_tareas = None

    # Gráficos de Barras para tareas y proyectos
    estados_tareas = ['Completadas', 'No Completadas']
    conteo_tareas = [
        tareas.filter(completada=True).count(),
        tareas.filter(completada=False).count()
    ]
    fig_barras_tareas = go.Figure(data=[go.Bar(
        x=estados_tareas, 
        y=conteo_tareas, 
        marker_color=['#66BB6A', '#EF5350'],  # Verde para completadas, rojo para no completadas
        text=conteo_tareas,
        textposition='auto'
    )])
    fig_barras_tareas.update_layout(title='Tareas Completadas vs No Completadas', xaxis_title='Estado', yaxis_title='Cantidad')

    estados_proyectos = ['En_progreso', 'Completado', 'Pendiente']
    conteo_proyectos = [proyectos.filter(estado=estado.lower()).count() for estado in estados_proyectos]
    fig_barras_proyectos = go.Figure(data=[go.Bar(
        x=estados_proyectos, 
        y=conteo_proyectos, 
        marker_color=['#FFA726', '#66BB6A', '#EF5350'],  # Naranja para en progreso, verde para completado, rojo para pendiente
        text=conteo_proyectos,
        textposition='auto'
    )])
    fig_barras_proyectos.update_layout(title='Proyectos por Estado', xaxis_title='Estado', yaxis_title='Cantidad')

    # Gráficos de Pastel para tareas y proyectos
    fig_pastel_tareas = go.Figure(data=[go.Pie(
        labels=estados_tareas, 
        values=conteo_tareas, 
        hole=0.3, 
        marker=dict(colors=['#66BB6A', '#EF5350']),  # Verde para completadas, rojo para no completadas
        textinfo='label+percent'
    )])
    fig_pastel_tareas.update_layout(title='Distribución de Tareas Completadas vs No Completadas')

    fig_pastel_proyectos = go.Figure(data=[go.Pie(
        labels=estados_proyectos, 
        values=conteo_proyectos, 
        hole=0.3, 
        marker=dict(colors=['#FFA726', '#66BB6A', '#EF5350']),  # Naranja para en progreso, verde para completado, rojo para pendiente
        textinfo='label+percent'
    )])
    fig_pastel_proyectos.update_layout(title='Distribución de Proyectos por Estado')

    # Gráfico de Dispersión de Proyectos por fecha de inicio y fin
    fechas_inicio = [proyecto.fecha_inicio for proyecto in proyectos if proyecto.fecha_inicio]
    fechas_fin = [proyecto.fecha_fin for proyecto in proyectos if proyecto.fecha_fin]

    fig_dispersion_proyectos = go.Figure()

    # Agregar puntos para las fechas de inicio
    fig_dispersion_proyectos.add_trace(go.Scatter(
        x=fechas_inicio, 
        y=[1 for _ in fechas_inicio],
        mode='markers',
        name='Fecha de Inicio',
        marker=dict(color='rgba(0, 128, 255, .8)')  # Azul para fechas de inicio
    ))

    # Agregar puntos para las fechas de fin
    fig_dispersion_proyectos.add_trace(go.Scatter(
        x=fechas_fin, 
        y=[1.5 for _ in fechas_fin],  # Ajuste para mostrar los puntos de fin un poco más arriba
        mode='markers',
        name='Fecha de Fin',
        marker=dict(color='rgba(255, 0, 0, .8)')  # Rojo para fechas de fin
    ))

    fig_dispersion_proyectos.update_layout(
        title='Dispersión de Proyectos por Fecha de Inicio y Fin',
        xaxis_title='Fecha',
        yaxis_title='Proyectos',
        yaxis=dict(showticklabels=False)  # Oculta las etiquetas del eje Y para simplificar
    )

    # Gráficos de Dispersión de Tareas por fecha de creación
    fechas_tareas = [tarea.fecha_creacion.date() for tarea in tareas]
    fig_dispersion_tareas = go.Figure(data=[go.Scatter(
        x=fechas_tareas, 
        y=[1 for _ in fechas_tareas],
        mode='markers',
        marker=dict(color='rgba(100, 200, 150, .8)')
    )])
    fig_dispersion_tareas.update_layout(title='Dispersión de Tareas por Fecha', xaxis_title='Fecha', yaxis_title='Cantidad')

    # Renderizar gráficos
    return render(request, 'directora/reportes.html', {
        'grafico_barras_tareas': plot(fig_barras_tareas, output_type='div'),
        'grafico_barras_proyectos': plot(fig_barras_proyectos, output_type='div'),
        'grafico_pastel_tareas': plot(fig_pastel_tareas, output_type='div'),
        'grafico_pastel_proyectos': plot(fig_pastel_proyectos, output_type='div'),
        'grafico_dispersion_tareas': plot(fig_dispersion_tareas, output_type='div'),
        'grafico_dispersion_proyectos': plot(fig_dispersion_proyectos, output_type='div'),
        'empleados': empleados,
        'rol': rol,
        'empleado_mas_tareas': empleado_mas_tareas,
        'tareas_empleado_mas_tareas': tareas_empleado_mas_tareas
    })


def generar_pdf(request):
    # Renderizamos la plantilla HTML
    html_string = render_to_string('directora/reportes_pdf.html', {
        'proyectos': Proyecto.objects.all(),
        'tareas': Tarea.objects.all(),
    })
    
    # Crear PDF a partir del HTML
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte.pdf"'

    pisa_status = pisa.CreatePDF(
        html_string, dest=response
    )
    
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status=500)
    
    return response

def exportar_excel(request):
    proyectos = Proyecto.objects.all()
    tareas = Tarea.objects.all()

    data = {
        'Título Proyecto': [proyecto.titulo for proyecto in proyectos],
        'Estado Proyecto': [proyecto.estado for proyecto in proyectos],
        'Título Tarea': [tarea.titulo for tarea in tareas],
        'Estado Tarea': ['Completada' if tarea.completada else 'Pendiente' for tarea in tareas]
    }
    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte.xlsx"'
    df.to_excel(response, index=False)
    return response
