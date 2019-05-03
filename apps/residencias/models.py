from django.db import models
import datetime


class Residencia(models.Model):
    nombre = models.CharField(
        max_length=255
    )
    fecha_ocupacion = models.DateField(
        default=datetime.date.today,
        verbose_name="Fecha de ocupación"
    )
    fecha_publicacion = models.DateField(
        default=datetime.date.today
    )
    foto = models.URLField()
    precio_base = models.FloatField()
    descripcion = models.TextField(
        verbose_name="Descripción"
    )
    ubicacion = models.CharField(
        max_length=255,
        verbose_name="Ubicación"
    )

    def __str__(self):
        return self.nombre
