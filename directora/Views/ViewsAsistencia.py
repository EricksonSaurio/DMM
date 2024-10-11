from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from directora.models import Asistencia
import pytz

# Función para obtener el rol del usuario autenticado
def obtener_rol(user):
    if user.groups.filter(name='Directora').exists():
        return 'Directora'
    elif user.groups.filter(name='Asistente').exists():
        return 'Asistente'
    elif user.groups.filter(name='Técnica de Campo').exists():
        return 'Técnica de Campo'
    else:
        return 'default'

# Vista del menú de asistencia con el rol del usuario
@login_required
def menu_asistencia(request):
    rol = obtener_rol(request.user)
    return render(request, 'directora/asistencia/menu_asistencia.html', {'rol': rol})

# Vista para registrar la entrada con el rol del usuario
@login_required
def registrar_entrada(request):
    mensaje = None
    guatemala_tz = pytz.timezone('America/Guatemala')
    rol = obtener_rol(request.user)

    if request.method == 'POST':
        # Obtén la hora actual ajustada a la zona horaria de Guatemala
        ahora = timezone.now().astimezone(guatemala_tz)
        fecha_actual = ahora.date()

        asistencia, created = Asistencia.objects.get_or_create(
            empleado=request.user,
            fecha=fecha_actual,
            defaults={'hora_entrada': ahora.time(), 'estado': 'Presente'}
        )
        mensaje = 'Entrada registrada correctamente' if created else 'Ya has registrado tu entrada para hoy'
    
    return render(request, 'directora/asistencia/registrar_entrada.html', {'mensaje': mensaje, 'rol': rol})

# Vista para registrar la salida con el rol del usuario
@login_required
def registrar_salida(request):
    mensaje = None
    guatemala_tz = pytz.timezone('America/Guatemala')
    rol = obtener_rol(request.user)

    if request.method == 'POST':
        try:
            asistencia = Asistencia.objects.get(
                empleado=request.user,
                fecha=timezone.now().date()
            )
            asistencia.hora_salida = timezone.now().astimezone(guatemala_tz).time()
            asistencia.save()
            mensaje = 'Salida registrada correctamente'
        except Asistencia.DoesNotExist:
            mensaje = 'No se encontró un registro de entrada para hoy. Registre su entrada antes de salir.'
        
        return render(request, 'directora/asistencia/registrar_salida.html', {'mensaje': mensaje, 'rol': rol})
    
    return render(request, 'directora/asistencia/registrar_salida.html', {'mensaje': mensaje, 'rol': rol})


@login_required
def historial_asistencia(request):
    # Obtener el rol del usuario autenticado
    rol = obtener_rol(request.user)

    # Si el usuario es Directora, obtiene todas las asistencias, de lo contrario solo las del usuario
    if rol == 'Directora':
        asistencias = Asistencia.objects.select_related('empleado').all().order_by('-fecha')
    else:
        asistencias = Asistencia.objects.filter(empleado=request.user).order_by('-fecha')

    # Renderizar la plantilla con los registros de asistencia y el rol
    return render(request, 'directora/asistencia/historial_asistencia.html', {
        'asistencias': asistencias,
        'rol': rol
    })