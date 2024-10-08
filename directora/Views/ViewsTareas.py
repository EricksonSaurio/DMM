from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Empleado, PerfilUsuario, Tarea, Notificacion
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.conf import settings

def obtener_rol(user):
    if user.groups.filter(name='Directora').exists():
        return 'Directora'
    elif user.groups.filter(name='Asistente').exists():
        return 'Asistente'
    elif user.groups.filter(name='Técnica de Campo').exists():
        return 'Técnica de Campo'
    else:
        return 'default'
    
# Vista del menú de tareas
@login_required
def menu_tareas(request):
    rol = obtener_rol(request.user)
    return render(request, 'directora/Tareas/menu_tareas.html', {'rol': rol})

# Vista para asignar una tarea
@login_required
def asignar_tarea(request):
    rol = obtener_rol(request.user)
    
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
            return redirect('listar_tareas')

        except Empleado.DoesNotExist:
            messages.error(request, 'El empleado seleccionado no existe.')
        except PerfilUsuario.DoesNotExist:
            messages.error(request, 'No se encontró un perfil de usuario para el empleado seleccionado.')

    empleados = Empleado.objects.all()  # Lista de empleados
    return render(request, 'directora/Tareas/asignar_tarea.html', {'empleados': empleados, 'rol': rol})

# Vista para mostrar notificaciones no leídas
@login_required
def mostrar_notificaciones(request):
    rol = obtener_rol(request.user)
    notificaciones = Notificacion.objects.filter(usuario=request.user, leida=False)
    return render(request, 'directora/Tareas/notificaciones.html', {'notificaciones': notificaciones, 'rol': rol})

# Función para enviar una notificación por correo electrónico al asignar una tarea
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
    html_content = render_to_string('directora/Tareas/tarea_asignada.html', {
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

# Vista para listar tareas
@login_required
def listar_tareas(request):
    usuario = request.user
    rol = obtener_rol(usuario)
    
    # Si el usuario es parte del grupo "Directora", obtiene todas las tareas
    if rol == 'Directora':
        tareas = Tarea.objects.all()
    else:
        # Si no, solo las tareas asignadas a ese usuario
        tareas = Tarea.objects.filter(asignada_a=usuario)
    
    return render(request, 'directora/Tareas/listar_tareas.html', {'tareas': tareas, 'rol': rol})
