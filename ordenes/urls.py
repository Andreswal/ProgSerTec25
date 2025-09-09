from django.urls import path
from . import views

urlpatterns = [
    path('crear-marca/', views.crear_marca, name='crear_marca'),
    path('nuevo-equipo/', views.nuevo_equipo, name='nuevo_equipo'),
    path('crear-modelo/', views.crear_modelo, name='crear_modelo'),
    path('crear-tipo-equipo/', views.crear_tipo_equipo, name='crear_tipo_equipo'),
    path('api/tipos-equipo/', views.obtener_tipos_equipo, name='obtener_tipos_equipo'),

]
