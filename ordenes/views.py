from django.shortcuts import render, redirect
from .forms import EquipoForm

def nuevo_equipo(request):
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('alguna_ruta')
    else:
        form = EquipoForm()
    return render(request, 'ordenes/nuevo_equipo.html', {'form': form})
