from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse

def iniciar_sesion(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('username')
        contraseña = request.POST.get('password')
        usuario = authenticate(request, username=nombre_usuario, password=contraseña)
        
        if usuario is not None:
            login(request, usuario)
            return redirect('inicio')  # Redirige a la página de inicio después del login
        else:
            # Si la autenticación falla, vuelve a mostrar el formulario con un mensaje de error
            return render(request, 'login/login.html', {
                'error': 'Credenciales inválidas',
            })

    # Para solicitudes GET, simplemente muestra el formulario de login
    return render(request, 'login/login.html')

