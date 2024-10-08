from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Proyecto
from ..forms import ProyectoForm

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
def menu_gestion_proyectos(request):
    rol = obtener_rol(request.user)
    return render(request, 'directora/Proyectos/menu_gestion_proyectos.html', {'rol': rol})
   
@login_required
def listar_proyectos(request):
    rol = obtener_rol(request.user)
    proyectos = Proyecto.objects.all()
    return render(request, 'directora/Proyectos/listar_proyectos.html', {'proyectos': proyectos, 'rol': rol})

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
    return render(request, 'directora/Proyectos/crear_proyecto.html', {'form': form, 'rol': rol})

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
    return render(request, 'directora/Proyectos/editar_proyecto.html', {'form': form, 'proyecto': proyecto, 'rol': rol})

@login_required
def eliminar_proyecto(request, proyecto_id):
    rol = obtener_rol(request.user)
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        proyecto.delete()
        return redirect('listar_proyectos')
    return render(request, 'directora/Proyectos/eliminar_proyecto.html', {'proyecto': proyecto, 'rol': rol})
