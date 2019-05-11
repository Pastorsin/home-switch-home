from django.db import models
from django.contrib.contenttypes.models import ContentType
from residencias.models import Residencia
import datetime


class Estado(models.Model):
    class Meta:
        abstract = True

    def residencia(self):
        """Devuelve la residencia que contiene este estado"""
        estado_actual = ContentType.objects.get_for_model(self.__class__)
        residencias = Residencia.objects.filter(
            estado_id=self.id, content_type=estado_actual)
        primera_residencia = residencias.values()[0]
        return primera_residencia

    def es_compra_directa(self):
        return False

    def es_subasta(self):
        return False


class CompraDirecta(Estado):
    def __str__(self):
        return 'Compra directa'

    def es_compra_directa(self):
        return True


class Subasta(Estado):
    fecha_inicio = models.DateField(
        default=datetime.date.today
    )
    fecha_cierre = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return 'En subasta'

    def es_subasta(self):
        return True

    def precio_actual(self):
        # Query
        # 1º Reusar Estado>>residencia
        # 2º Filtrar la reserva por la residencia de 1º
        return "200000"

    def ganador_actual(self):
        # Query
        return "Goffredo"
