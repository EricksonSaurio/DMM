from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from directora.models import Tarea, Empleado, Asistencia,  PerfilUsuario
from django.utils import timezone
import pytz



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
def tareas_asignadas(request):
    # Obtener el rol del usuario actual.
    rol = obtener_rol(request.user)
    
    # Obtener las tareas asignadas al usuario actual.
    tareas = Tarea.objects.filter(asignada_a=request.user)

    if request.method == 'POST':
        tarea_id = request.POST.get('tarea_id')
        tarea = get_object_or_404(Tarea, id=tarea_id, asignada_a=request.user)
        tarea.completada = True
        tarea.save()
        return redirect('tareas_asignadas')  # Redirigir después de marcar la tarea como completada

    return render(request, 'asistente/tareas_asignadas.html', {'tareas': tareas, 'rol': rol})
# Create your views here.

@login_required
def menu_asistencia_asistente(request):
    rol = obtener_rol(request.user)
    return render(request, 'asistente/menu_asistencia_asistente.html', {'rol': rol})

@login_required
def marcar_entrada_asistente(request):
    mensaje = None
    guatemala_tz = pytz.timezone('America/Guatemala')
    rol = obtener_rol(request.user)

    # Verificar que el rol del usuario sea "Asistente"
    if rol != 'Asistente':
        mensaje = 'No tienes permiso para registrar una entrada.'
        return render(request, 'asistente/error.html', {'mensaje': mensaje})

    if request.method == 'POST':
        # Obtén la hora actual ajustada a la zona horaria de Guatemala
        ahora = timezone.now().astimezone(guatemala_tz)
        fecha_actual = ahora.date()

        asistencia, created = Asistencia.objects.get_or_create(
            empleado=request.user,
            fecha=fecha_actual,
            defaults={'hora_entrada': ahora.time(), 'estado': 'Presente'}
        )
        mensaje = 'Entrada registrada correctamente' if created else 'Ya has registrado tu entrada para hoy.'
    
    return render(request, 'asistente/registrar_entrada_asistente.html', {'mensaje': mensaje, 'rol': rol})

@login_required
def marcar_salida_asistente(request):
    mensaje = None
    guatemala_tz = pytz.timezone('America/Guatemala')
    rol = obtener_rol(request.user)

    # Verificar que el rol del usuario sea "Asistente"
    if rol != 'Asistente':
        mensaje = 'No tienes permiso para registrar una salida.'
        return render(request, 'asistente/error.html', {'mensaje': mensaje})

    if request.method == 'POST':
        # Ajustar la hora actual a la zona horaria de Guatemala
        ahora = timezone.now().astimezone(guatemala_tz)
        fecha_actual = ahora.date()

        try:
            # Busca el registro de asistencia para la fecha de hoy y el usuario actual
            asistencia = Asistencia.objects.get(
                empleado=request.user,
                fecha=fecha_actual
            )
            
            # Verifica si la hora de entrada ya está registrada antes de permitir la salida
            if asistencia.hora_entrada:
                if asistencia.hora_salida:
                    mensaje = 'Ya has registrado tu salida para hoy.'
                else:
                    asistencia.hora_salida = ahora.time()
                    asistencia.save()
                    mensaje = 'Salida registrada correctamente.'
            else:
                mensaje = 'No se encontró un registro de entrada para hoy. Registre su entrada antes de salir.'
        
        except Asistencia.DoesNotExist:
            mensaje = 'No se encontró un registro de entrada para hoy. Registre su entrada antes de salir.'

        return render(request, 'asistente/registrar_salida_asistente.html', {'mensaje': mensaje, 'rol': rol})

    return render(request, 'asistente/registrar_salida_asistente.html', {'mensaje': mensaje, 'rol': rol})

@login_required
def ver_asistencia_asistente(request):
    # Obtiene el perfil del usuario actual
    perfil_usuario = get_object_or_404(PerfilUsuario, user=request.user)

    # Asegúrate de que el perfil tenga un empleado asociado
    if perfil_usuario.empleado is None:
        return render(request, 'asistente/error.html', {
            'mensaje': 'No tienes un empleado asociado para ver la asistencia.'
        })

    # Obtiene la instancia de Empleado desde el perfil de usuario
    empleado = perfil_usuario.empleado

    # Filtra las asistencias del empleado actual
    asistencias = Asistencia.objects.filter(empleado=request.user)

    return render(request, 'asistente/ver_asistencia_asistente.html', {'asistencias': asistencias})