from django.shortcuts import render
from .models import Proyecto
from directora.models import Proyecto


def tracking_proyectos(request):
    proyectos = Proyecto.objects.all()
    
    # Asignar avance según el estado del proyecto
    for proyecto in proyectos:
        if proyecto.estado == 'en_progreso':
            proyecto.avance = 50
        elif proyecto.estado == 'completado':
            proyecto.avance = 100
        elif proyecto.estado == 'pendiente':
            proyecto.avance = 0

    return render(request, 'informacion/informacion.html', {'proyectos': proyectos})


def proyectos_realizados(request):
    proyectos = Proyecto.objects.all().prefetch_related('imagenes')
    return render(request, 'informacion/informacion.html', {'proyectos': proyectos})