from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

from residencias.models import Residencia
from accounts.models import CustomUser

from django.urls import reverse
from django.db import models

from datetime import date, timedelta


class EventoNoPermitido(Exception):
    pass


class Semana(models.Model):

    residencia = models.ForeignKey(
        Residencia,
        on_delete=models.CASCADE
    )
    fecha_inicio = models.DateField(
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

    def cambiar_estado(self, estado):
        if self.estado is not None:
            self.estado.delete()

        self.estado = estado
        self.estado_id = estado.pk
        self.save()

    def dar_de_baja(self):
        return self.estado.dar_de_baja()

    def abrir_subasta(self):
        return self.estado.abrir_subasta()

    def cerrar_subasta(self):
        return self.estado.cerrar_subasta()

    def establecer_hotsale(self):
        pass

    def comprar(self):
        pass

    def detalle_estado(self):
        return self.estado.detalle()

    def __str__(self):
        return 'Semana {} con estado {}'.format(
                self.numero, self.estado)

    class Meta:
         unique_together = ('content_type', 'estado_id')



class Estado(models.Model):

    semanas = GenericRelation(
        Semana,
        content_type_field='content_type',
        object_id_field='estado_id'
    )

    @property
    def semana(self):
        return self.semanas.first()

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
    def dar_de_baja(self):
        no_disponible = NoDisponible.objects.create()
        self.semana.cambiar_estado(no_disponible)
        return 'Se ha dado de baja la semana correctamente'

    def detalle(self):
        raise NotImplementedError('Método abstracto, implementame')

    def abrir_subasta(self):
        raise NotImplementedError('Método abstracto, implementame')

    def cerrar_subasta(self):
        raise NotImplementedError('Método abstracto, implementame')

    def __str__(self):
        raise NotImplementedError('Método abstracto, implementame')

    class Meta:
        abstract = True


class NoDisponible(Estado):

    def __str__(self):
        return 'No disponible'

    def es_no_disponible(self):
        return True

    def dar_de_baja(self):
        raise EventoNoPermitido('La semana ya se encuentra dada de baja')

    def abrir_subasta(self):
        pass

    def cerrar_subasta(self):
        pass

    def detalle(self):
        return ''


class CompraDirecta(Estado):

    def __str__(self):
        return 'Compra directa'

    def es_compra_directa(self):
        return True

    def dar_de_baja(self):
        super().dar_de_baja()

    def abrir_subasta(self):
        SEMANAS_MINIMAS = 26  # 6 meses = 26 semanas
        tiempo_transcurrido = date.today() - self.semana.residencia.fecha_publicacion
        if tiempo_transcurrido >= timedelta(weeks=SEMANAS_MINIMAS):
            precio_base = self.semana.residencia.precio_base
            subasta = Subasta.objects.create(precio_actual=precio_base)
            self.semana.cambiar_estado(subasta)
            return 'Se ha puesto la semana en subasta correctamente'
        else:
            error = 'La semana debe estar como mínimo 6 meses ' +\
                'en compra directa'
            raise EventoNoPermitido(error)

    def cerrar_subasta(self):
        pass

    def detalle(self):
        return ''


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
    ganador_actual = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
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

    def dar_de_baja(self):
        raise EventoNoPermitido('No se puede dar de baja una subasta activa')

    def abrir_subasta(self):
        pass

    def cerrar_subasta(self):
        if self.hay_ganador():
            reservada = Reservada.objects.create(
                precio_actual=self.precio_actual,
                ganador_actual=self.ganador_actual
            )
            self.semana.cambiar_estado(reservada)
        else:
            en_espera = EnEspera.objects.create()
            self.semana.cambiar_estado(en_espera)
        return 'Se ha cerrado la subasta correctamente'

    def detalle(self):
        return ''


class EnEspera(Estado):

    def __str__(self):
        return 'En espera'

    def es_en_espera(self):
        return True

    def dar_de_baja(self):
        super().dar_de_baja()

    def abrir_subasta(self):
        pass

    def cerrar_subasta(self):
        pass

    def detalle(self):
        return ''


class Reservada(Estado):
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
        return 'Reservada'

    def es_reservada(self):
        return True

    def dar_de_baja(self):
        raise EventoNoPermitido('La semana se encuentra reservada')

    def abrir_subasta(self):
        pass

    def cerrar_subasta(self):
        pass

    def detalle(self):
        return 'por {} con un monto de ${}'.format(
            self.ganador_actual,
            self.precio_actual)
