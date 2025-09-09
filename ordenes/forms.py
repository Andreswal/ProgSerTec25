from django import forms
from .models import Equipo
from .models import TipoEquipo

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

from django import forms
from .models import Marca

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre']

from .models import Modelo

class ModeloForm(forms.ModelForm):
    class Meta:
        model = Modelo
        fields = ['nombre', 'marca']
        
class TipoEquipoForm(forms.ModelForm):
    class Meta:
        model = TipoEquipo
        fields = ['nombre']