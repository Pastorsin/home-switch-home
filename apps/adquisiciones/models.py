from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from residencias.models import Residencia
from datetime import date, timedelta


class Estado(models.Model):

    @property
    def residencia(self):
        """Devuelve la residencia que contiene este estado"""
        estado_actual = ContentType.objects.get_for_model(self.__class__)
        try:
            residencia = Residencia.objects.get(
                estado_id=self.id, content_type=estado_actual)
        except Residencia.DoesNotExist:
            return None
        return residencia

    def es_compra_directa(self):
        return False

    def es_subasta(self):
        return False

    def es_no_disponible(self):
        return False

    class Meta:
        abstract = True


class NoDisponible(Estado):

    def __str__(self):
        return 'No disponible'

    def es_no_disponible(self):
        return True


class CompraDirecta(Estado):

    def __str__(self):
        return 'Compra directa'

    def es_compra_directa(self):
        return True


class Subasta(Estado):
    fecha_inicio = models.DateField(
        default=date.today
    )
    fecha_cierre = models.DateField(
        default=date.today() + timedelta(days=3),
        null=True,
        blank=True
    )
    puja_actual = models.FloatField(
        null=True,
        blank=True
    )
    ganador_actual = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    def __str__(self):
        return 'Subasta'

    def es_subasta(self):
        return True

    def precio_actual(self):
        # Query
        # 1º Reusar Estado>>residencia
        # 2º Filtrar la reserva por la residencia de 1º
        precio_actual = self.puja_actual
        precio_base = self.residencia.precio_base
        return precio_actual if precio_actual else precio_base

    def precio_minimo(self):
        return self.precio_actual() + 0.1

    def nueva_puja(self, nuevo_pujador, nuevo_precio):
        # self.ganador_actual.incrementar_credito()
        self.ganador_actual = nuevo_pujador
        self.puja_actual = nuevo_precio
        # nuevo_pujador.decrementar_credito()
        self.save()

    def hay_ganador(self):
        # Query
        return bool(self.ganador_actual)

    def get_absolute_url(self):
        return reverse('mostrar_subasta', args=[str(self.pk)])
