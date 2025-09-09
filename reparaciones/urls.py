from django.urls import path
from ordenes import views as ordenes_views

urlpatterns = [
    path('nuevo-equipo/', ordenes_views.nuevo_equipo, name='nuevo_equipo'),
    path('ajax/modelos/', ordenes_views.modelos_por_marca, name='ajax_modelos'),
]

