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
from django.contrib import messages
from .models import Tarea
from django.core.mail import send_mail
from .models import Notificacion
from premailer import transform
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from premailer import Premailer
import os
from django.conf import settings
from .models import Tarea, Empleado, PerfilUsuario

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
    # Obtiene el rol del usuario actual
    rol = obtener_rol(request.user)
    
    if request.method == 'POST':
        # Si el método de la solicitud es POST, crea un formulario con los datos enviados
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            # Si el formulario es válido, guarda el nuevo empleado
            form.save()
            # Muestra un mensaje de éxito
            messages.success(request, 'Empleado agregado exitosamente.')
            # Redirige a la misma vista para evitar re-envío del formulario
            return redirect('agregar_empleado')
        else:
            # Si el formulario no es válido, muestra un mensaje de error
            messages.error(request, 'Ocurrió un error al agregar el empleado.')
    else:
        # Si el método de la solicitud no es POST, crea un formulario vacío
        form = EmpleadoForm()

    # Renderiza la plantilla 'agregar_empleado.html' con el formulario y el rol del usuario
    return render(request, 'directora/agregar_empleado.html', {'form': form, 'rol': rol})

@login_required
def ver_empleados(request):
    rol = obtener_rol(request.user)
    empleados = Empleado.objects.all()  # Obtener todos los empleados
    return render(request, 'directora/ver_empleados.html', {'empleados': empleados, 'rol': rol})

@login_required
def editar_empleado(request, empleado_id):
    # Obtiene el rol del usuario actual
    rol = obtener_rol(request.user)
    
    # Obtiene el empleado a editar o devuelve un error 404 si no existe
    empleado = get_object_or_404(Empleado, id=empleado_id)
    
    if request.method == 'POST':
        # Si el método de la solicitud es POST, crea un formulario con los datos enviados y el empleado existente
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            # Si el formulario es válido, guarda los cambios en el empleado
            form.save()
            # Muestra un mensaje de éxito
            messages.success(request, 'Empleado actualizado exitosamente.')
            # Redirige a la vista de ver empleados
            return redirect('ver_empleados')
        else:
            # Si el formulario no es válido, muestra un mensaje de error
            messages.error(request, 'Ocurrió un error al actualizar el empleado.')
    else:
        # Si el método de la solicitud no es POST, crea un formulario con los datos del empleado existente
        form = EmpleadoForm(instance=empleado)
    
    # Renderiza la plantilla 'editar_empleado.html' con el formulario, el rol del usuario y los datos del empleado
    return render(request, 'directora/editar_empleado.html', {'form': form, 'rol': rol, 'empleado': empleado})

# Vista para eliminar un empleado
@login_required
def eliminar_empleado(request, empleado_id):
    # Obtiene el rol del usuario actual
    rol = obtener_rol(request.user)
    
    # Obtiene el empleado a eliminar o devuelve un error 404 si no existe
    empleado = get_object_or_404(Empleado, id=empleado_id)
    
    if request.method == 'POST':
        # Si el método de la solicitud es POST, elimina el empleado
        empleado.delete()
        # Muestra un mensaje de éxito
        messages.success(request, 'Empleado eliminado exitosamente.')
        # Redirige a la vista de ver empleados
        return redirect('ver_empleados')
    
    # Renderiza la plantilla 'eliminar_empleado.html' con los datos del empleado y el rol del usuario
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

    try:
        # Intenta obtener el empleado relacionado con el correo del usuario
        empleado = Empleado.objects.get(correo=user.email)
    except Empleado.DoesNotExist:
        empleado = None

    if request.method == 'POST':
        form = UsuarioEmpleadoForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('ver_usuarios')
    else:
        # Si existe el empleado, lo pasamos como valor inicial del campo 'empleado'
        initial_data = {'empleado': empleado}
        form = UsuarioEmpleadoForm(instance=user, initial=initial_data)

    return render(request, 'directora/editar_usuario.html', {'form': form, 'user_id': user_id, 'rol': rol, 'empleado': empleado})


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
    # Obtiene el rol del usuario actual
    rol = obtener_rol(request.user)
    
    # Obtiene los 10 usuarios más recientes, ordenados por la fecha de creación en orden descendente
    usuarios_recientes = User.objects.all().order_by('-date_joined')[:10]
    
    # Obtiene los 10 usuarios más antiguos, ordenados por la fecha de creación en orden ascendente
    usuarios_antiguos = User.objects.all().order_by('date_joined')[:10]
    
    # Obtiene los 10 usuarios eliminados más recientes, ordenados por la fecha de eliminación en orden descendente
    usuarios_eliminados = UsuarioEliminado.objects.all().order_by('-fecha_eliminacion')[:10]

    # Renderiza la plantilla 'informe_usuarios.html' con los datos de los usuarios y el rol del usuario
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

@login_required
def menu_tareas(request):
    rol = obtener_rol(request.user)
    return render(request, 'directora/menu_tareas.html', {'rol': rol})

def asignar_tarea(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        fecha_limite = request.POST.get('fecha_limite')
        empleado_id = request.POST.get('empleado')

        try:
            # Obtener el empleado seleccionado
            empleado = Empleado.objects.get(id=empleado_id)
            # Obtener el perfil de usuario asociado al empleado
            perfil = PerfilUsuario.objects.get(empleado=empleado)

            # Crear la tarea y asignarla al usuario relacionado
            tarea = Tarea.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                fecha_limite=fecha_limite,
                asignada_a=perfil.user  # Asegurar que la tarea se asigna al usuario
            )

            # Llamar a la función para enviar el correo al usuario relacionado
            enviar_notificacion_correo(request, empleado, tarea)

            # Notificaciones o mensajes
            messages.success(request, f'Tarea "{titulo}" asignada correctamente a {empleado.nombre} {empleado.apellido}')
            return redirect('listar_tareas.html')

        except Empleado.DoesNotExist:
            messages.error(request, 'El empleado seleccionado no existe.')
        except PerfilUsuario.DoesNotExist:
            messages.error(request, 'No se encontró un perfil de usuario para el empleado seleccionado.')

    empleados = Empleado.objects.all()  # Lista de empleados
    return render(request, 'directora/asignar_tarea.html', {'empleados': empleados})


def mostrar_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user, leida=False)
    return render(request, 'directora/notificaciones.html', {'notificaciones': notificaciones})

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.conf import settings
from .models import PerfilUsuario

@login_required
def enviar_notificacion_correo(request, empleado, tarea):
    rol = obtener_rol(request.user)
    subject = f'Nueva tarea asignada: {tarea.titulo}'
    from_email = settings.DEFAULT_FROM_EMAIL

    # Obtener el usuario relacionado con el empleado
    perfil = PerfilUsuario.objects.get(empleado=empleado)
    to = perfil.user.email  # Usar el correo del usuario relacionado

    if not to:
        print(f"El empleado {empleado.nombre} {empleado.apellido} no tiene un correo asignado.")
        return

    # Obtener la URL del sitio actual para generar las URLs completas
    current_site = Site.objects.get_current()
    logo_url = f'http://{current_site.domain}/static/images/logo.png'
    dashboard_url = f'http://{current_site.domain}/directora/listar-tareas/'

    # Renderizar la plantilla HTML con el CSS embebido en la plantilla
    html_content = render_to_string('directora/tarea_asignada.html', {
        'empleado': empleado,
        'tarea': tarea,
        'logo_url': logo_url,
        'dashboard_url': dashboard_url,
        'rol': rol,
    })

    # Crear el correo electrónico con contenido HTML y texto alternativo
    email = EmailMultiAlternatives(subject, 'Se te ha asignado una nueva tarea. Por favor, revisa el dashboard.', from_email, [to])
    email.attach_alternative(html_content, "text/html")
    
    # Enviar el correo
    email.send()

@login_required
def listar_tareas(request):
    usuario = request.user
    
    # Si el usuario es parte del grupo "Directora", obtiene todas las tareas
    if usuario.groups.filter(name='Directora').exists():
        tareas = Tarea.objects.all()
    else:
        # Si no, solo las tareas asignadas a ese usuario
        tareas = Tarea.objects.filter(asignado_a=usuario)
    
    return render(request, 'directora/listar_tareas.html', {'tareas': tareas})