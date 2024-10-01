# directora/urls.py
from django.urls import path #type: ignore
from . import views

urlpatterns = [
    path('empleados/', views.empleados, name='empleados'),  # Cambia empleados_view a empleados
    path('agregar_empleado/', views.agregar_empleado, name='agregar_empleado'),
    path('ver_empleados/', views.ver_empleados, name='ver_empleados'),
    path('informes/', views.informes, name='informes'),
    path('menu/', views.menu_gestion_proyectos, name='menu_gestion_proyectos'),
    path('proyectos/', views.listar_proyectos, name='listar_proyectos'),
    path('crear_proyecto/', views.crear_proyecto, name='crear_proyecto'),
    path('editar/<int:proyecto_id>/', views.editar_proyecto, name='editar_proyecto'),
    path('eliminar/<int:proyecto_id>/', views.eliminar_proyecto, name='eliminar_proyecto'),
    path('agregar_usuario/', views.agregar_usuario, name='agregar_usuario'),
    path('ver_usuarios/', views.ver_usuarios, name='ver_usuarios'),
    path('editar_usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('informe_usuarios/', views.informe_usuarios, name='informe_usuarios'),
    path('get-email/<int:empleado_id>/', views.get_empleado_email, name='get-empleado-email'),
    path('editar_empleado/<int:empleado_id>/', views.editar_empleado, name='editar_empleado'),
    path('eliminar_empleado/<int:empleado_id>/', views.eliminar_empleado, name='eliminar_empleado'),
    path('dashboard/', views.dashboard_proyectos, name='dashboard_proyectos'),
    path('exportar_proyectos_excel/', views.exportar_proyectos_excel, name='exportar_proyectos_excel'),
    path('exportar_proyectos_excel_grafico/', views.exportar_proyectos_excel_con_grafico, name='exportar_proyectos_excel_grafico'),
    path('asignar_tarea/', views.asignar_tarea, name='asignar_tarea'),
    path('listar_tareas/', views.listar_tareas, name='listar_tareas'), 
]
