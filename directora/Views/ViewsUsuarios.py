from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ..forms import UsuarioEmpleadoForm
from ..models import UsuarioEliminado, Empleado, PerfilUsuario

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
def agregar_usuario(request):
    rol = obtener_rol(request.user)
    if request.method == 'POST':
        form = UsuarioEmpleadoForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Usuario agregado exitosamente.')
            return redirect('agregar_usuario')
    else:
        form = UsuarioEmpleadoForm()
    return render(request, 'directora/Usuarios/agregar_usuario.html', {'form': form, 'rol': rol})

@login_required
def ver_usuarios(request):
    rol = obtener_rol(request.user)
    usuarios = User.objects.all()
    return render(request, 'directora/Usuarios/ver_usuarios.html', {'usuarios': usuarios, 'rol': rol})

@login_required
def editar_usuario(request, user_id):
    rol = obtener_rol(request.user)
    user = get_object_or_404(User, pk=user_id)

    # Obtenemos el perfil existente o lanzamos un 404 si no existe
    perfil_usuario = PerfilUsuario.objects.filter(user=user).first()

    if request.method == 'POST':
        form = UsuarioEmpleadoForm(request.POST, instance=user)
        if form.is_valid():
            # Guardamos los datos del formulario de usuario
            form.save()

            # Si el perfil ya existe, lo actualizamos; de lo contrario, lo creamos
            if perfil_usuario:
                perfil_usuario.empleado = form.cleaned_data.get('empleado')
                perfil_usuario.save()
            else:
                PerfilUsuario.objects.create(user=user, empleado=form.cleaned_data.get('empleado'))

            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('ver_usuarios')
    else:
        initial_data = {'empleado': perfil_usuario.empleado if perfil_usuario else None}
        form = UsuarioEmpleadoForm(instance=user, initial=initial_data)

    return render(request, 'directora/Usuarios/editar_usuario.html', {
        'form': form,
        'user_id': user_id,
        'rol': rol,
        'empleado': perfil_usuario.empleado if perfil_usuario else None
    })




@login_required
def eliminar_usuario(request, user_id):
    rol = obtener_rol(request.user)
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        UsuarioEliminado.objects.create(username=user.username, email=user.email)
        user.delete()
        return redirect('ver_usuarios')
    return render(request, 'directora/Usuarios/eliminar_usuario.html', {'user': user, 'rol': rol})

@login_required
def informe_usuarios(request):
    # Obtiene el rol del usuario actual
    rol = obtener_rol(request.user)
    
    # Obtiene los 10 usuarios más recientes, ordenados por la fecha de creación en orden descendente
    usuarios_recientes = User.objects.all().order_by('-date_joined')[:10]
    
    # Obtiene los 10 usuarios más antiguos, ordenados por la fecha de creación en orden ascendente
    usuarios_antiguos = User.objects.all().order_by('date_joined')[:10]
    
    # Obtiene los 10 usuarios eliminados más recientes, ordenados por la fecha de eliminación en orden descendente
    usuarios_eliminados = UsuarioEliminado.objects.all().order_by('-fecha_eliminacion')[:10]

    # Renderiza la plantilla 'informe_usuarios.html' con los datos de los usuarios y el rol del usuario
    return render(request, 'directora/Usuarios/informe_usuarios.html', {
        'usuarios_recientes': usuarios_recientes,
        'usuarios_antiguos': usuarios_antiguos,
        'usuarios_eliminados': usuarios_eliminados,
        'rol': rol
    })