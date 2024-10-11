from django.urls import path
from . import views

urlpatterns = [
    path('tareas/', views.tareas_asignadas, name='tareas_asignadas'),
    path('asistencia/menu/', views.menu_asistencia, name='menu_asistencia'),
    path('asistencia/', views.ver_asistencia, name='ver_asistencia'),
    path('asistencia/marcar_entrada/', views.marcar_entrada, name='marcar_entrada'),
    path('asistencia/marcar_salida/', views.marcar_salida, name='marcar_salida'),
    # Otras rutas si las hay...
]
