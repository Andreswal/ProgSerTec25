from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


# 📋 Orden de trabajo asociada a un equipo
class OrdenTrabajo(models.Model):
    ESTADO_CHOICES = [
        ('ingresado', 'Ingresado'),
        ('revision', 'En revisión'),
        ('presupuestado', 'Presupuestado'),
        ('reparado', 'Reparado'),
        ('no_reparable', 'No Reparable'),
        ('espera_repuesto', 'En espera de repuesto'),
        ('demorado', 'Demorado'),
        ('retirado', 'Retirado'),  # ✅ nuevo estado agregado
    ]

    equipo = models.ForeignKey('Equipo', on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ingresado')
    diagnostico_tecnico = models.TextField(blank=True)
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.estado}"

class TipoEquipo(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Modelo(models.Model):
    nombre = models.CharField(max_length=50)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('nombre', 'marca')  # Evita duplicados por marca

    def __str__(self):
        return self.nombre

# 🧍 Cliente
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, default="Sin teléfono")
    telefono_alternativo = models.CharField(max_length=20, blank=True, default="Sin alternativo")
    email = models.EmailField(blank=True, default="sin_email@ejemplo.com")
    direccion = models.CharField(max_length=200, blank=True, default="Sin dirección")
    provincia = models.CharField(max_length=100, blank=True, default="Sin provincia")
    ciudad = models.CharField(max_length=100, blank=True, default="Sin ciudad")
    observaciones = models.TextField(blank=True, default="Sin observaciones")

    def __str__(self):
        return self.nombre



# 📱 Equipo ingresado por el cliente
class Equipo(models.Model):
    TIPO_CHOICES = [
        ('celular', 'Celular'),
        ('tablet', 'Tablet'),
        ('otro', 'Otro'),
    ]

    tipo = models.ForeignKey(TipoEquipo, on_delete=models.SET_NULL, null=True)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True)
    modelo = models.ForeignKey(Modelo, on_delete=models.SET_NULL, null=True)
    imei = models.CharField(max_length=30, blank=True)
    numero_serie = models.CharField(max_length=30, blank=True)
    accesorios = models.TextField(blank=True)
    estado_visual = models.TextField(blank=True)
    falla_declarada = models.TextField()
    fecha_compra = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    en_garantia = models.BooleanField(default=False)
    fuera_garantia_por_uso = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.tipo})"

    # 🔍 Validación personalizada para evitar duplicados activos
    def clean(self):
        if self.imei:
            equipos = Equipo.objects.filter(imei=self.imei).exclude(id=self.id)
            for eq in equipos:
                ordenes = OrdenTrabajo.objects.filter(equipo=eq).exclude(estado='retirado')
                if ordenes.exists():
                    raise ValidationError({
                        'imei': f"Este IMEI ya está en una orden activa (estado: {ordenes.first().estado})."
                    })

        if self.numero_serie:
            equipos = Equipo.objects.filter(numero_serie=self.numero_serie).exclude(id=self.id)
            for eq in equipos:
                ordenes = OrdenTrabajo.objects.filter(equipo=eq).exclude(estado='retirado')
                if ordenes.exists():
                    raise ValidationError({
                        'numero_serie': f"Este número de serie ya está en una orden activa (estado: {ordenes.first().estado})."
                    })

    # 💾 Guardado personalizado: valida y crea orden automáticamente
    def save(self, *args, **kwargs):
        self.full_clean()  # Ejecuta las validaciones del método clean()
        
        # 🧮 Calcular si está en garantía (menos de 1 año desde la fecha de compra)
        if self.fecha_compra:
            diferencia = date.today() - self.fecha_compra
            self.en_garantia = diferencia.days <= 365
        else:
            self.en_garantia = False

        crear_orden = self.pk is None
        super().save(*args, **kwargs)

        if crear_orden:
            OrdenTrabajo.objects.create(equipo=self)

