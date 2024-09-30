from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def pagina_inicio(request):
    user = request.user
    rol = None
    
    if user.groups.filter(name='Directora').exists():
        rol = 'Directora'
    elif user.groups.filter(name='Asistente').exists():
        rol = 'Asistente'
    elif user.groups.filter(name='Técnica de Campo').exists():
        rol = 'Técnica de Campo'
    
    return render(request, 'inicio/index.html', {'rol': rol})
