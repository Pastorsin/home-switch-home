from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    estado_id = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    estado = GenericForeignKey(
        'content_type',
        'estado_id'
    )

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('detalle_residencia', args=[str(self.pk)])

    def cambiar_estado(self, estado):
        if self.estado is not None:
            self.estado.delete()

        self.estado = estado
        self.estado_id = estado.pk
        self.save()

    def eliminar(self):
        return self.estado.eliminar()

    def abrir_subasta(self):
        return self.estado.abrir_subasta()

    def cerrar_subasta(self):
        return self.estado.cerrar_subasta()

    def establecer_hotsale(self):
        pass

    class Meta:
        ordering = ['-fecha_publicacion', 'precio_base']
