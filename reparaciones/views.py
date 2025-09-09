# reparaciones/views.py

from django.shortcuts import render

from django.http import JsonResponse
from ordenes.models import Modelo


def modelos_por_marca(request):
    marca_id = request.GET.get('marca_id')
    modelos = Modelo.objects.filter(marca_id=marca_id).values('id', 'nombre')
    return JsonResponse(list(modelos), safe=False)


# Podés agregar tus vistas acá más adelante
