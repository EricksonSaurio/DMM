from django.urls import path
from . import views

urlpatterns = [
    path('tareas/', views.tareas_asignadas, name='tareas_asignadas'),
    path('asistencia/menu/', views.menu_asistencia_asistente, name='menu_asistencia_asistente'),
    path('asistencia/', views.ver_asistencia_asistente, name='ver_asistencia_asistente'),
    path('asistencia/marcar_entrada/', views.marcar_entrada_asistente, name='marcar_entrada_asistente'),
    path('asistencia/marcar_salida/', views.marcar_salida_asistente, name='marcar_salida_asistente'),
    # Otras rutas si las hay...
]
