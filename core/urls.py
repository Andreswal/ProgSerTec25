
from django.contrib import admin
from django.urls import path, include
from ordenes import views


urlpatterns = [
    path('admin/', admin.site.urls),  # 👈 Panel de administración
    path('', include('reparaciones.urls')),  # 👈 Rutas de tu app principal
    path('ordenes/', include('ordenes.urls')),
    path('listar/', views.listar_ordenes, name='listar_ordenes'),


]


