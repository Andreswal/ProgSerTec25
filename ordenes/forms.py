from django import forms
from .models import Equipo

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = [
            'cliente',         # 👈 aparece primero
            'tipo',
            'marca',
            'modelo',
            'imei',
            'numero_serie',
            'accesorios',
            'estado_visual',
            'falla_declarada',
            'fecha_compra',
        ]
