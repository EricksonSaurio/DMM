# directora/urls.py
from django.urls import path
from directora.Views import ViewsEmpleado #type: ignore
from directora.Views import views, ViewsProyectos, ViewsUsuarios, ViewsDashboard, ViewsTareas, ViewsReportes, ViewsAsistencia


urlpatterns = [
    path('empleados/', ViewsEmpleado.empleados, name='empleados'),  # Cambia empleados_view a empleados
    path('agregar_empleado/', ViewsEmpleado.agregar_empleado, name='agregar_empleado'),
    path('ver_empleados/', ViewsEmpleado.ver_empleados, name='ver_empleados'),
    path('editar_empleado/<int:empleado_id>/', ViewsEmpleado.editar_empleado, name='editar_empleado'),
    path('eliminar_empleado/<int:empleado_id>/', ViewsEmpleado.eliminar_empleado, name='eliminar_empleado'),
    path('informes/', ViewsEmpleado.informes, name='informes'),
    path('menu/', ViewsProyectos.menu_gestion_proyectos, name='menu_gestion_proyectos'),
    path('proyectos/', ViewsProyectos.listar_proyectos, name='listar_proyectos'),
    path('crear_proyecto/', ViewsProyectos.crear_proyecto, name='crear_proyecto'),
    path('editar/<int:proyecto_id>/', ViewsProyectos.editar_proyecto, name='editar_proyecto'),
    path('eliminar/<int:proyecto_id>/', ViewsProyectos.eliminar_proyecto, name='eliminar_proyecto'),
    path('agregar_usuario/', ViewsUsuarios.agregar_usuario, name='agregar_usuario'),
    path('ver_usuarios/', ViewsUsuarios.ver_usuarios, name='ver_usuarios'),
    path('editar_usuario/<int:user_id>/', ViewsUsuarios.editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:user_id>/', ViewsUsuarios.eliminar_usuario, name='eliminar_usuario'),
    path('informe_usuarios/', ViewsUsuarios.informe_usuarios, name='informe_usuarios'),
    path('get-email/<int:empleado_id>/', ViewsEmpleado.get_empleado_email, name='get-empleado-email'),
    path('dashboard/', ViewsDashboard.dashboard_proyectos, name='dashboard_proyectos'),
    path('exportar_proyectos_excel/', ViewsDashboard.exportar_proyectos_excel, name='exportar_proyectos_excel'),
    path('exportar_proyectos_excel_grafico/', ViewsDashboard.exportar_proyectos_excel_con_grafico, name='exportar_proyectos_excel_grafico'),
    path('asignar_tarea/', ViewsTareas.asignar_tarea, name='asignar_tarea'),
    path('listar_tareas/', ViewsTareas.listar_tareas, name='listar_tareas'), 
    path('menu_tareas/', ViewsTareas.menu_tareas, name='menu_tareas'),
    path('reporte/', ViewsReportes.reporte_proyectos, name='reporte_proyectos'),
    path('reporte/pdf/', ViewsReportes.generar_pdf, name='generar_pdf'),
    path('reporte/excel/', ViewsReportes.exportar_excel, name='exportar_excel'),
    path('reporte/csv/', ViewsReportes.exportar_csv, name='exportar_csv'),
    path('asistencia/menu/', ViewsAsistencia.menu_asistencia, name='menu_asistencia'),
    path('asistencia/entrada/', ViewsAsistencia.registrar_entrada, name='registrar_entrada'),
    path('asistencia/salida/', ViewsAsistencia.registrar_salida, name='registrar_salida'),
    path('asistencia/historial/', ViewsAsistencia.historial_asistencia, name='historial_asistencia'),
]

