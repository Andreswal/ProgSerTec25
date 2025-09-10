
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ordenes.urls')),  # 👈 Esto conecta la raíz con tu vista 'inicio'
]
