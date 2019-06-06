from django.db import models
from django.urls import reverse
import datetime


class Ubicacion(models.Model):
    class Meta:
        unique_together = ('pais', 'provincia', 'ciudad', 'calle', 'numero')

    pais = models.CharField(
        max_length=255
    )
    provincia = models.CharField(
        max_length=255
    )
    ciudad = models.CharField(
        max_length=255
    )
    calle = models.CharField(
        max_length=255
    )
    numero = models.IntegerField()

    def __str__(self):
        return "{calle} {numero}, {pais}, {provincia}, {ciudad}".format(
            pais=self.pais,
            provincia=self.provincia,
            ciudad=self.ciudad,
            calle=self.calle,
            numero=self.numero
        )


class Residencia(models.Model):

    nombre = models.CharField(
        max_length=255
    )
    fecha_publicacion = models.DateField(
        default=datetime.date.today
    )
    foto = models.URLField(
    )
    precio_base = models.FloatField(
        verbose_name="Precio"
    )
    descripcion = models.TextField(
        verbose_name="Descripción"
    )
    ubicacion = models.OneToOneField(
        Ubicacion,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    SEMANAS_TOTALES = 52

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('detalle_residencia', args=[str(self.pk)])

    def crear_semanas(self):
        from adquisiciones.models import Semana
        for numero_semana in range(0, self.SEMANAS_TOTALES):
            semana = Semana.objects.create(
                residencia=self
            )
            semana.inicializar_con(numero_semana)

    @property
    def semanas(self):
        return self.semana_set.all()

    class Meta:
        ordering = ['-fecha_publicacion', 'precio_base']
