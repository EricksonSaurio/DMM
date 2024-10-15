from django.urls import path
from . import views

urlpatterns = [
    path('', views.tracking_proyectos, name='tracking_proyectos'),
    path('', views.proyectos_realizados, name='proyectos_realizados'),
    
]
