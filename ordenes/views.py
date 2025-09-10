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
            return redirect('listar_equipos')
    else:
        form = EquipoForm()
    return render(request, 'ordenes/nuevo_equipo.html', {'form': form})

from django.http import JsonResponse
from .models import Modelo, Marca

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

from .forms import ClienteForm

def crear_cliente(request):
    form = ClienteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('nuevo_equipo')  # Redirige al formulario principal
    return render(request, 'ordenes/crear_cliente.html', {'form': form})

# Vista del panel principal
def inicio(request):
    return render(request, 'ordenes/inicio.html')

from .models import Equipo

def listar_equipos(request):
    equipos = Equipo.objects.all()
    return render(request, 'ordenes/listar_equipos.html', {'equipos': equipos})

from .models import Cliente

def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'ordenes/listar_clientes.html', {'clientes': clientes})

def formulario_equipo(request):
    form = EquipoForm()
    return render(request, 'ordenes/partials/form_equipo.html', {'form': form})

from django.shortcuts import render, redirect
from .models import Cliente, Equipo, OrdenTrabajo

def crear_orden_trabajo(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        equipo_id = request.POST.get('equipo_id')
        falla = request.POST.get('falla_declarada')
        estado_visual = request.POST.get('estado_visual')

        cliente = Cliente.objects.get(id=cliente_id)
        equipo = Equipo.objects.get(id=equipo_id)

        orden = OrdenTrabajo.objects.create(
            equipo=equipo,
            diagnostico_tecnico='',
            presupuesto=None,
            estado_visual=estado_visual,
            falla_declarada=falla
        )

        return redirect('inicio')  # Volver al panel principal

    clientes = Cliente.objects.all()
    equipos = Equipo.objects.all()
    return render(request, 'ordenes/form_orden_trabajo.html', {
        'clientes': clientes,
        'equipos': equipos
    })

from .forms import ClienteForm
from django.http import JsonResponse

def crear_cliente_modal(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            return JsonResponse({'success': True, 'cliente_id': cliente.id, 'cliente_nombre': cliente.nombre})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ClienteForm()
        return render(request, 'ordenes/partials/form_cliente.html', {'form': form})

from .forms import EquipoForm

def crear_equipo_modal(request):
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            equipo = form.save()
            return JsonResponse({'success': True, 'equipo_id': equipo.id, 'equipo_nombre': str(equipo)})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = EquipoForm()
        return render(request, 'ordenes/partials/form_equipo.html', {'form': form})


from .forms import ClienteForm, EquipoForm
from .forms import EquipoForm

def formulario_orden(request):
    clientes = Cliente.objects.all()
    equipos = Equipo.objects.all()
    cliente_form = ClienteForm()
    equipo_form = EquipoForm()

    return render(request, 'ordenes/partials/form_orden_trabajo.html', {
        'clientes': clientes,
        'equipos': equipos,
        'cliente_form': cliente_form,
        'equipo_form': equipo_form
    })

from django.http import JsonResponse
from .models import OrdenTrabajo, Cliente, Equipo

def guardar_orden_ajax(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        equipo_id = request.POST.get('equipo_id')
        falla = request.POST.get('falla_declarada')
        estado = request.POST.get('estado_visual')

        orden = OrdenTrabajo.objects.create(
            cliente_id=cliente_id,
            equipo_id=equipo_id,
            falla_declarada=falla,
            estado_visual=estado
        )
        return JsonResponse({'success': True, 'orden_id': orden.id})
    return JsonResponse({'success': False}, status=400)

from django.http import JsonResponse
from django.http import JsonResponse

def guardar_cliente_ajax(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            return JsonResponse({'success': True, 'id': cliente.id, 'nombre': cliente.nombre})
    return JsonResponse({'success': False})

def guardar_equipo_ajax(request):
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            equipo = form.save()
            return JsonResponse({'success': True, 'id': equipo.id, 'nombre': str(equipo)})
    return JsonResponse({'success': False})
