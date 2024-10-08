
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Proyecto, Tarea
from django.http import HttpResponse
from xhtml2pdf import pisa  # Cambiar la biblioteca para generar PDFs
import pandas as pd
from django.template.loader import render_to_string

from django.utils import timezone
from datetime import datetime

from ..models import PerfilUsuario

import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render
from ..models import Proyecto, Tarea, Empleado
from datetime import datetime
from django.utils import timezone

import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render
from ..models import Proyecto, Tarea, Empleado
from datetime import datetime
from django.utils import timezone

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

    # Filtros
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    empleado_id = request.GET.get('empleado')

    empleados = Empleado.objects.all()
    proyectos = Proyecto.objects.all()
    tareas = Tarea.objects.all()

    if fecha_inicio and fecha_fin:
        # Convertir las fechas a aware con zona horaria
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        fecha_inicio_aware = timezone.make_aware(fecha_inicio_dt)
        fecha_fin_aware = timezone.make_aware(fecha_fin_dt)

        # Filtrar tareas por empleado y fechas
        if empleado_id and empleado_id != "":
            # Buscar el usuario relacionado con el empleado seleccionado
            perfil_usuario = PerfilUsuario.objects.filter(empleado_id=empleado_id).first()
            if perfil_usuario:
                tareas = tareas.filter(asignada_a=perfil_usuario.user).filter(fecha_creacion__range=[fecha_inicio_aware, fecha_fin_aware])
            else:
                tareas = Tarea.objects.none()  # Si no hay perfil asociado, no devolver tareas
        else:
            tareas = tareas.filter(fecha_creacion__range=[fecha_inicio_aware, fecha_fin_aware])

    # Depuración: Verificar cuántas tareas se están filtrando
    print(f"Tareas filtradas: {tareas.count()}")
    print(f"Proyectos filtradas: {proyectos.count()}")
    # Generar gráfico de proyectos por estado
    estados_proyectos = ['en_progreso', 'completado', 'pendiente']
    conteo_proyectos = [proyectos.filter(estado=estado).count() for estado in estados_proyectos]

    if sum(conteo_proyectos) > 0:
        plt.figure(figsize=(10, 6))
        plt.bar(estados_proyectos, conteo_proyectos, color=['#FF9800', '#4CAF50', '#F44336'])
        plt.title('Proyectos por Estado')
        plt.xlabel('Estado')
        plt.ylabel('Cantidad')

        buf_proyectos = io.BytesIO()
        plt.savefig(buf_proyectos, format='png')
        buf_proyectos.seek(0)
        string_proyectos = base64.b64encode(buf_proyectos.read())
        uri_proyectos = urllib.parse.quote(string_proyectos)
    else:
        uri_proyectos = None

    # Generar gráfico de tareas completadas vs no completadas
    estados_tareas = ['true', 'false']
    conteo_tareas = [
        tareas.filter(completada=True).count(),
        tareas.filter(completada=False).count()
    ]

    if sum(conteo_tareas) > 0:
        plt.figure(figsize=(10, 6))
        plt.bar(estados_tareas, conteo_tareas, color=['#4CAF50', '#FF9800'])
        plt.title('Tareas Completadas vs No Completadas')
        plt.xlabel('Estado de Tareas')
        plt.ylabel('Cantidad')

        buf_tareas = io.BytesIO()
        plt.savefig(buf_tareas, format='png')
        buf_tareas.seek(0)
        string_tareas = base64.b64encode(buf_tareas.read())
        uri_tareas = urllib.parse.quote(string_tareas)
    else:
        uri_tareas = None

    return render(request, 'directora/reportes.html', {
        'data_grafico_proyectos': uri_proyectos,
        'data_grafico_tareas': uri_tareas,  # Agregar el gráfico de tareas
        'empleados': empleados,
        'rol': rol  # Agregar el rol al contexto
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
