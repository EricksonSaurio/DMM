from django.contrib import messages
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.shortcuts import get_object_or_404, redirect # type: ignore
from networkx import difference # type: ignore
from .models import Proyecto
from .forms import ProyectoForm
from .forms import UsuarioEmpleadoForm
from django.shortcuts import render # type: ignore
from django.contrib.auth.models import User # type: ignore
from .models import UsuarioEliminado
import openpyxl
from openpyxl.chart import BarChart, Reference, series
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.fill import ColorChoice
from django.http import HttpResponse
from .models import Proyecto
from directora.models import Empleado
from .forms import EmpleadoForm
from django.http import JsonResponse

def obtener_rol(user):
    if user.groups.filter(name='Directora').exists():
        return 'Directora'
    elif user.groups.filter(name='Asistente').exists():
        return 'Asistente'
    elif user.groups.filter(name='Técnica de Campo').exists():
        return 'Técnica de Campo'
    else:
        return 'default'

# Vista para gestionar empleados
@login_required
def empleados(request):
    rol = obtener_rol(request.user)
    return render(request, 'directora/empleados.html', {'rol': rol})

# Vista para agregar un empleado
@login_required
def agregar_empleado(request):
    rol = obtener_rol(request.user)
    
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado agregado exitosamente.')
            return redirect('agregar_empleado')
        else:
            messages.error(request, 'Ocurrió un error al agregar el empleado.')
    else:
        form = EmpleadoForm()

    return render(request, 'directora/agregar_empleado.html', {'form': form, 'rol': rol})

@login_required
def ver_empleados(request):
    rol = obtener_rol(request.user)
    empleados = Empleado.objects.all()  # Obtener todos los empleados
    return render(request, 'directora/ver_empleados.html', {'empleados': empleados, 'rol': rol})

@login_required
def editar_empleado(request, empleado_id):
    rol = obtener_rol(request.user)
    empleado = get_object_or_404(Empleado, id=empleado_id)
    
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado actualizado exitosamente.')
            return redirect('ver_empleados')
        else:
            messages.error(request, 'Ocurrió un error al actualizar el empleado.')
    else:
        form = EmpleadoForm(instance=empleado)
    
    return render(request, 'directora/editar_empleado.html', {'form': form, 'rol': rol, 'empleado': empleado})

@login_required
def eliminar_empleado(request, empleado_id):
    rol = obtener_rol(request.user)
    empleado = get_object_or_404(Empleado, id=empleado_id)
    
    if request.method == 'POST':
        empleado.delete()
        messages.success(request, 'Empleado eliminado exitosamente.')
        return redirect('ver_empleados')
    
    return render(request, 'directora/eliminar_empleado.html', {'empleado': empleado, 'rol': rol})

@login_required
def informes(request):
    rol = obtener_rol(request.user)

    if request.method == 'POST':
        tipo_informe = request.POST.get('tipo_informe')
        if tipo_informe == 'departamento':
            empleados = Empleado.objects.order_by('departamento')
        elif tipo_informe == 'fecha_contratacion':
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')
            empleados = Empleado.objects.filter(fecha_contratacion__range=[fecha_inicio, fecha_fin])
        else:
            empleados = Empleado.objects.all()

        return render(request, 'directora/informes_resultados.html', {'empleados': empleados, 'rol': rol})
    return render(request, 'directora/informes.html', {'rol': rol})

@login_required
def listar_proyectos(request):
    rol = obtener_rol(request.user)
    proyectos = Proyecto.objects.all()
    return render(request, 'directora/listar_proyectos.html', {'proyectos': proyectos, 'rol': rol})

@login_required
def crear_proyecto(request):
    rol = obtener_rol(request.user)

    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proyecto creado exitosamente.')
        else:
            messages.error(request, 'Ocurrió un error al crear el proyecto.')
    else:
        form = ProyectoForm()
    return render(request, 'directora/crear_proyecto.html', {'form': form, 'rol': rol})

@login_required
def editar_proyecto(request, proyecto_id):
    rol = obtener_rol(request.user)
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('listar_proyectos')
    else:
        form = ProyectoForm(instance=proyecto)
    return render(request, 'directora/editar_proyecto.html', {'form': form, 'proyecto': proyecto, 'rol': rol})

@login_required
def eliminar_proyecto(request, proyecto_id):
    rol = obtener_rol(request.user)
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    if request.method == 'POST':
        proyecto.delete()
        return redirect('listar_proyectos')
    return render(request, 'directora/eliminar_proyecto.html', {'proyecto': proyecto, 'rol': rol})

@login_required
def menu_gestion_proyectos(request):
    rol = obtener_rol(request.user)
    return render(request, 'directora/menu_gestion_proyectos.html', {'rol': rol})

from django.shortcuts import render, redirect  # type: ignore
from .forms import UsuarioEmpleadoForm


@login_required
def agregar_usuario(request):
    rol = obtener_rol(request.user)
    
    if request.method == 'POST':
        form = UsuarioEmpleadoForm(request.POST)
        if form.is_valid():
            # Crea el usuario
            user = form.save()
            messages.success(request, 'Usuario agregado exitosamente.')
            return redirect('agregar_usuario')  # Redirige para evitar re-envío del formulario
    else:
        form = UsuarioEmpleadoForm()
    
    return render(request, 'directora/agregar_usuario.html', {'form': form, 'rol': rol})


@login_required
def ver_usuarios(request):
    rol = obtener_rol(request.user)
    usuarios = User.objects.all()  # Obtiene todos los usuarios
    return render(request, 'directora/ver_usuarios.html', {'usuarios': usuarios, 'rol': rol})


@login_required
def editar_usuario(request, user_id):
    rol = obtener_rol(request.user)
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UsuarioEmpleadoForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('ver_usuarios')
    else:
        form = UsuarioEmpleadoForm(instance=user)
    return render(request, 'directora/editar_usuario.html', {'form': form, 'user_id': user_id, 'rol': rol})


def eliminar_usuario(request, user_id):
        rol = obtener_rol(request.user)
        user = get_object_or_404(User, pk=user_id)
        if request.method == 'POST':
            # Registra el usuario eliminado
            UsuarioEliminado.objects.create(username=user.username, email=user.email)
            user.delete()
            return redirect('ver_usuarios')
        return render(request, 'directora/eliminar_usuario.html', {'user': user, 'rol': rol})

@login_required
def listar_usuarios(request):
        rol = obtener_rol(request.user)
        usuarios = User.objects.all()
        return render(request, 'directora/listar_usuarios.html', {'usuarios': usuarios, 'rol': rol})

@login_required
def informe_usuarios(request):
    rol = obtener_rol(request.user)
    
    # Usuarios más recientes
    usuarios_recientes = User.objects.all().order_by('-date_joined')[:10]  # Últimos 10 usuarios creados
    # Usuarios más antiguos
    usuarios_antiguos = User.objects.all().order_by('date_joined')[:10]  # Primeros 10 usuarios creados
    # Usuarios eliminados (si se ha implementado)
    usuarios_eliminados = UsuarioEliminado.objects.all().order_by('-fecha_eliminacion')[:10]

    return render(request, 'directora/informe_usuarios.html', {
        'usuarios_recientes': usuarios_recientes,
        'usuarios_antiguos': usuarios_antiguos,
        'usuarios_eliminados': usuarios_eliminados,
        'rol': rol
    })

def get_empleado_email(request, empleado_id):
    try:
        empleado = Empleado.objects.get(pk=empleado_id)
        return JsonResponse({'correo': empleado.correo})
    except Empleado.DoesNotExist:
        return JsonResponse({'error': 'Empleado no encontrado'}, status=404)

@login_required
def dashboard_proyectos(request):
    rol = obtener_rol(request.user)
    proyectos_pendientes = Proyecto.objects.filter(estado='pendiente').count()
    proyectos_en_progreso = Proyecto.objects.filter(estado='en_progreso').count()
    proyectos_terminados = Proyecto.objects.filter(estado='completado').count()
    
    context = {
        'proyectos_pendientes': proyectos_pendientes,
        'proyectos_en_progreso': proyectos_en_progreso,
        'proyectos_terminados': proyectos_terminados,
        'rol': rol
    }
    
    return render(request, 'directora/dashboard_proyectos.html', context)


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



def exportar_proyectos_excel_con_grafico(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Proyectos'

    # Encabezados
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

    # Rango de datos para el gráfico
    data = Reference(ws, min_col=2, min_row=1, max_row=2, max_col=4)  # Cada columna es una serie
    categories = Reference(ws, min_col=1, min_row=2, max_row=2)  # Categoría (nombre de los estados)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(categories)

    # Colores personalizados para cada serie (estado)
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

