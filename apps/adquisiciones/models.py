from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from residencias.models import Residencia
from datetime import date, timedelta


class EventoNoPermitido(Exception):
    pass


class Estado(models.Model):

    class Meta:
        abstract = True

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

    # Querys
    def es_compra_directa(self):
        return False

    def es_subasta(self):
        return False

    def es_no_disponible(self):
        return False

    def es_en_espera(self):
        return False

    def es_reservada(self):
        return False

    # Eventos
    def eliminar(self):
        raise Exception('Método abstracto, implementame')

    def abrir_subasta(self):
        raise Exception('Método abstracto, implementame')

    def cerrar_subasta(self):
        raise Exception('Método abstracto, implementame')


class NoDisponible(Estado):

    def __str__(self):
        return 'No disponible'

    def es_no_disponible(self):
        return True

    def eliminar(self):
        pass

    def abrir_subasta(self):
        pass

    def cerrar_subasta(self):
        pass


class CompraDirecta(Estado):

    def __str__(self):
        return 'Compra directa'

    def es_compra_directa(self):
        return True

    def eliminar(self):
        no_disponible = NoDisponible.objects.create()
        self.residencia.cambiar_estado(no_disponible)
        return 'Se ha eliminado la residencia correctamente'

    def abrir_subasta(self):
        # SEMANAS_MINIMAS = 26  # 6 meses = 26 semanas
        # tiempo_transcurrido = date.today() - residencia.fecha_publicacion
        # tiempo_transcurrido >= timedelta(weeks=self.SEMANAS_MINIMAS)
        if True:
            precio_base = self.residencia.precio_base
            subasta = Subasta.objects.create(precio_actual=precio_base)
            self.residencia.cambiar_estado(subasta)
            return 'Se ha puesto la residencia en subasta correctamente'
        else:
            error = 'La residencia debe estar como mínimo 6 meses ' +\
                'en compra directa'
            raise EventoNoPermitido(error)

    def cerrar_subasta(self):
        pass


class Subasta(Estado):
    fecha_inicio = models.DateField(
        default=date.today
    )
    fecha_cierre = models.DateField(
        default=date.today() + timedelta(days=3),
        null=True,
        blank=True
    )
    precio_actual = models.FloatField(
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

    def precio_minimo(self):
        return self.precio_actual + 0.1

    def nueva_puja(self, nuevo_pujador, nuevo_precio):
        # self.ganador_actual.incrementar_credito()
        self.ganador_actual = nuevo_pujador
        self.precio_actual = nuevo_precio
        # nuevo_pujador.decrementar_credito()
        self.save()

    def hay_ganador(self):
        return bool(self.ganador_actual)

    def get_absolute_url(self):
        return reverse('mostrar_subasta', args=[str(self.pk)])

    def eliminar(self):
        raise EventoNoPermitido('No se puede eliminar en una subasta')

    def abrir_subasta(self):
        pass

    def cerrar_subasta(self):
        if self.residencia.estado.hay_ganador():
            reservada = Reservada.objects.create()
            self.residencia.cambiar_estado(reservada)
        else:
            en_espera = EnEspera.objects.create()
            self.residencia.cambiar_estado(en_espera)
        return 'Se ha cerrado la subasta correctamente'


class EnEspera(Estado):

    def __str__(self):
        return 'En espera'

    def es_en_espera(self):
        return True

    def eliminar(self):
        no_disponible = NoDisponible.objects.create()
        self.residencia.cambiar_estado(no_disponible)
        return 'Se ha eliminado la residencia correctamente'

    def abrir_subasta(self):
        pass

    def cerrar_subasta(self):
        pass


class Reservada(Estado):

    def __str__(self):
        return 'Reservada'

    def es_reservada(self):
        return True

    def eliminar(self):
        pass

    def abrir_subasta(self):
        pass

    def cerrar_subasta(self):
        pass
