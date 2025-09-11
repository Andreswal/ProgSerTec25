from django.urls import path
from . import views

urlpatterns = [
    path('crear-marca/', views.crear_marca, name='crear_marca'),
    path('nuevo-equipo/', views.nuevo_equipo, name='nuevo_equipo'),
    path('crear-modelo/', views.crear_modelo, name='crear_modelo'),
    path('crear-tipo-equipo/', views.crear_tipo_equipo, name='crear_tipo_equipo'),
    path('api/tipos-equipo/', views.obtener_tipos_equipo, name='obtener_tipos_equipo'),
    path('crear-cliente/', views.crear_cliente, name='crear_cliente'),
    path('', views.inicio, name='inicio'),
    path('equipos/', views.listar_equipos, name='listar_equipos'),
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('ajax/modelos/', views.modelos_por_marca, name='ajax_modelos'),
    path('equipo/formulario/', views.formulario_equipo, name='formulario_equipo'),
    path('orden/nueva/', views.crear_orden_trabajo, name='crear_orden'),
    path('cliente/modal/', views.crear_cliente_modal, name='crear_cliente_modal'),
    path('equipo/modal/', views.crear_equipo_modal, name='crear_equipo_modal'),
    path('formulario/', views.formulario_orden, name='formulario_orden'),
    path('guardar/', views.guardar_orden_ajax, name='guardar_orden_ajax'),
    path('guardar-completo/', views.guardar_orden_completa, name='guardar_orden_completa'),
    path('clientes/listar/', views.listar_clientes_ajax, name='listar_clientes_ajax'),
    path('equipo/buscar/', views.buscar_equipo_por_serie, name='buscar_equipo_por_serie'),
    path('listar/', views.listar_ordenes, name='listar_ordenes'),

]


