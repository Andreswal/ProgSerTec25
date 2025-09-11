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


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import ClienteForm, EquipoForm
from .models import OrdenTrabajo

@csrf_exempt
def guardar_orden_completa(request):
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)
        equipo_form = EquipoForm(request.POST)

        if cliente_form.is_valid() and equipo_form.is_valid():
            cliente = cliente_form.save()
            equipo = equipo_form.save()

            orden = OrdenTrabajo.objects.create(
                cliente=cliente,
                equipo=equipo,
                falla_declarada=request.POST.get('falla_declarada', ''),
                estado_visual=request.POST.get('estado_visual', '')
            )

            return JsonResponse({'success': True, 'orden_id': orden.id})
        else:
            print("Errores al guardar:")
            print("Cliente:", cliente_form.errors)
            print("Equipo:", equipo_form.errors)
            return JsonResponse({'success': False, 'errores': {
                'cliente': cliente_form.errors,
                'equipo': equipo_form.errors
            }})


from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Cliente

def listar_clientes_ajax(request):
    clientes = Cliente.objects.all()
    html = render_to_string('ordenes/partials/lista_clientes.html', {'clientes': clientes})
    return JsonResponse({'html': html})

from django.http import JsonResponse
from .models import Equipo

def buscar_equipo_por_serie(request):
    serie = request.GET.get('numero_serie', '').strip()
    try:
        equipo = Equipo.objects.get(numero_serie=serie)
        data = {
            'imei': equipo.imei,
            'tipo': equipo.tipo.id,
            'marca': equipo.marca.id,
            'modelo': equipo.modelo.id,
            'accesorios': equipo.accesorios,
            'estado_visual': equipo.estado_visual,
            'falla_declarada': equipo.falla_declarada,
            'fecha_compra': equipo.fecha_compra.strftime('%Y-%m-%d') if equipo.fecha_compra else '',
            'en_garantia': equipo.en_garantia,
            'fuera_garantia_uso': equipo.fuera_garantia_por_uso
        }
        return JsonResponse({'existe': True, 'equipo': data})
    except Equipo.DoesNotExist:
        return JsonResponse({'existe': False})


from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import OrdenTrabajo

def listar_ordenes(request):
    ordenes = OrdenTrabajo.objects.select_related('equipo').order_by('-id')
    html = render_to_string('ordenes/partials/tabla_ordenes.html', {'ordenes': ordenes})
    return JsonResponse({'html': html})

