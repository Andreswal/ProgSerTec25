from django.contrib import admin
from .models import Cliente, Equipo, OrdenTrabajo
from .models import TipoEquipo
from .models import Marca
from .models import Modelo

@admin.register(TipoEquipo)
class TipoEquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email')
    search_fields = ('nombre', 'telefono')

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'marca', 'modelo', 'cliente')
    search_fields = ('marca', 'modelo', 'imei', 'numero_serie')

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    
@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca')
    search_fields = ('nombre',)
    list_filter = ('marca',)
    
@admin.register(OrdenTrabajo)
class OrdenTrabajoAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipo', 'estado', 'fecha_ingreso')
    list_filter = ('estado',)
    search_fields = ('equipo__marca', 'equipo__modelo')

