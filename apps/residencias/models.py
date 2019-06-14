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
    eliminada = models.BooleanField(
        default=False
    )
    SEMANAS_TOTALES = 52

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('detalle_residencia', args=[str(self.pk)])

    def crear_semanas(self):
        from adquisiciones.models import Semana
        for numero_semana in range(1, self.SEMANAS_TOTALES + 1):
            semana = Semana.objects.create(residencia=self)
            semana.inicializar_con(numero_semana)

    def actualizar(self):
        for semana in self.semanas_actualizables():
            semana.actualizar()

    def crear_nueva_semana(self):
        from adquisiciones.models import Semana
        semana = Semana.objects.create(
            residencia=self
        )
        semana.inicializar_con(self.SEMANAS_TOTALES)

    def semanas_actualizables(self):
        return filter(lambda semana: semana.es_actualizable(),
                      self.semanas)

    def semanas_adquiribles(self):
        return filter(lambda semana: semana.es_adquirible(),
                      self.semanas)

    def esta_en_subasta(self):
        return any(self.semanas_en_subasta())

    def semanas_en_subasta(self):
        return filter(lambda semana: semana.esta_en_subasta(),
                      self.semanas)

    def eliminar(self):
        self.eliminada = True
        return "Se ha eliminado la residencia correctamente"

    @property
    def semanas(self):
        return self.semana_set.all()

    class Meta:
        ordering = ['-fecha_publicacion', 'precio_base']
