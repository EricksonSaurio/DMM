from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render



class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    departamento = models.CharField(max_length=100)
    fecha_contratacion = models.DateField()
    dpi = models.CharField(max_length=13)  # Campo DPI con longitud de 13 caracteres

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    def editar(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save()

    def eliminar(self):
        self.delete()



class Proyecto(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completado', 'Completado'),
    ]

    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=50, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return self.nombre
    

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'
    

class UsuarioEliminado(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    fecha_eliminacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    


def dashboard_proyectos(request):
    proyectos_pendientes = Proyecto.objects.filter(estado='pendiente')
    proyectos_en_progreso = Proyecto.objects.filter(estado='en_progreso')
    proyectos_terminados = Proyecto.objects.filter(estado='terminado')
    
    return render(request, 'dashboard_proyectos.html', {
        'proyectos_pendientes': proyectos_pendientes,
        'proyectos_en_progreso': proyectos_en_progreso,
        'proyectos_terminados': proyectos_terminados
    })

class Tarea(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_limite = models.DateField()
    asignada_a = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tareas_asignadas')
    completada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)