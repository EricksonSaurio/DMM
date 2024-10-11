from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..models import Empleado
from ..forms import EmpleadoForm

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
def empleados(request):
    rol = obtener_rol(request.user)
    return render(request, 'directora/Empleados/empleados.html', {'rol': rol})

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
    return render(request, 'directora/Empleados/agregar_empleado.html', {'form': form, 'rol': rol})

@login_required
def ver_empleados(request):
    rol = obtener_rol(request.user)
    empleados = Empleado.objects.all()
    return render(request, 'directora/Empleados/ver_empleados.html', {'empleados': empleados, 'rol': rol})

@login_required
def editar_empleado(request, empleado_id):
    rol = obtener_rol(request.user)  # Obtener el rol del usuario autenticado
    empleado = get_object_or_404(Empleado, id=empleado_id)  # Buscar al empleado por ID o retornar un 404 si no existe
    
    # Si la solicitud es POST, significa que el formulario fue enviado
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)  # Prellenar el formulario con la información enviada y la instancia del empleado
        if form.is_valid():  # Verificar si el formulario es válido
            form.save()  # Guardar los cambios en la base de datos
            messages.success(request, 'Empleado actualizado exitosamente.')
            return redirect('ver_empleados')  # Redirigir a la lista de empleados
        else:
            messages.error(request, 'Ocurrió un error al actualizar el empleado.')
    
    # Si es una solicitud GET, mostrar el formulario con la información actual del empleado
    else:
        form = EmpleadoForm(instance=empleado)  # Prellenar el formulario con la instancia del empleado
    
    # Renderizar la plantilla con el formulario prellenado y los datos del empleado
    return render(request, 'directora/Empleados/editar_empleado.html', {
        'form': form, 
        'rol': rol, 
        'empleado': empleado
    })

@login_required
def eliminar_empleado(request, empleado_id):
    rol = obtener_rol(request.user)
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        empleado.delete()
        messages.success(request, 'Empleado eliminado exitosamente.')
        return redirect('ver_empleados')
    return render(request, 'directora/Empleados/eliminar_empleado.html', {'empleado': empleado, 'rol': rol})


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

        return render(request, 'directora/Empleados/informes_resultados.html', {'empleados': empleados, 'rol': rol})
    return render(request, 'directora/Empleados/informes.html', {'rol': rol})

@login_required
def get_empleado_email(request, empleado_id):
    rol = obtener_rol(request.user)
    try:
        empleado = Empleado.objects.get(pk=empleado_id)
        return JsonResponse({'correo': empleado.correo, 'rol': rol})
    except Empleado.DoesNotExist:
        return JsonResponse({'error': 'Empleado no encontrado', 'rol': rol}, status=404)