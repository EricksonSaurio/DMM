from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse

def iniciar_sesion(request):
    # Verifica si el método de la solicitud es POST
    if request.method == 'POST':
        # Obtiene el nombre de usuario y la contraseña del formulario
        nombre_usuario = request.POST.get('username')
        contraseña = request.POST.get('password')
        
        # Autentica al usuario con las credenciales proporcionadas
        usuario = authenticate(request, username=nombre_usuario, password=contraseña)
        
        # Si la autenticación es exitosa
        if usuario is not None:
            # Inicia sesión para el usuario autenticado
            login(request, usuario)
            # Redirige a la página de inicio después del login
            return redirect('inicio')
        else:
            # Si la autenticación falla, vuelve a mostrar el formulario con un mensaje de error
            return render(request, 'login/login.html', {
                'error': 'Credenciales inválidas',
            })

    # Para solicitudes GET, simplemente muestra el formulario de login
    return render(request, 'login/login.html')

