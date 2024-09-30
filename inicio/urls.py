from django.urls import path
from .views import pagina_inicio

urlpatterns = [
    path('', pagina_inicio, name='inicio'),
]
