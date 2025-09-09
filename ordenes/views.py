from django.shortcuts import render, redirect
from .forms import EquipoForm
from .forms import MarcaForm
from .forms import ModeloForm
from .forms import TipoEquipoForm 

def nuevo_equipo(request):
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('alguna_ruta')
    else:
        form = EquipoForm()
    return render(request, 'ordenes/nuevo_equipo.html', {'form': form})

from django.http import JsonResponse
from .models import Modelo

def modelos_por_marca(request):
    marca_id = request.GET.get('marca_id')
    modelos = Modelo.objects.filter(marca_id=marca_id).values('id', 'nombre')
    return JsonResponse(list(modelos), safe=False)

from django.shortcuts import render, redirect

def crear_marca(request):
    form = MarcaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('nuevo_equipo')  # 👈 Redirige al formulario principal
    return render(request, 'ordenes/crear_marca.html', {'form': form})


from django.shortcuts import render

def crear_modelo(request):
    form = ModeloForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('nuevo_equipo')  # 👈 Redirige al formulario principal
    return render(request, 'ordenes/crear_modelo.html', {'form': form})

def crear_tipo_equipo(request):
    form = TipoEquipoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('nuevo_equipo')  # Redirige al formulario principal
    return render(request, 'ordenes/crear_tipo_equipo.html', {'form': form})

from django.http import JsonResponse
from .models import TipoEquipo

def obtener_tipos_equipo(request):
    tipos = TipoEquipo.objects.all().values('id', 'nombre')
    return JsonResponse(list(tipos), safe=False)