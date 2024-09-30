from django.shortcuts import render
from .models import Proyecto

def informacion(request):
    proyectos = Proyecto.objects.all().prefetch_related('imagenes')
    return render(request, 'informacion/informacion.html', {'proyectos': proyectos})
