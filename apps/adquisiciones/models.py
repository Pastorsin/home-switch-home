from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

from accounts.models import CustomUser
from residencias.models import Residencia

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
        null=True,
        blank=True
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
    seguidores = models.ManyToManyField(
        CustomUser,
        related_name='seguidores',
    )
    comprador = models.ForeignKey(
        CustomUser,
        related_name='comprador',
        on_delete=models.CASCADE,
        null=True
    )

    def inicializar_con(self, numero_semana):
        self.incializar_fecha(numero_semana)
        self.inicializar_estados()
        self.save()

    def incializar_fecha(self, numero_semana):
        self.fecha_inicio = self.generar_lunes(numero_semana)

    def generar_lunes(self, numero_semana):
        return self.lunes_actual() + timedelta(weeks=numero_semana)

    def lunes_actual(self):
        hoy = date.today()
        return hoy - timedelta(days=hoy.weekday())

    def inicializar_estados(self):
        Estado.crear(self)

    def estas_en_primer_mitad(self):
        semanas_totales = self.residencia.SEMANAS_TOTALES
        semanas_mitad = semanas_totales // 2
        return self.fecha_inicio < self.generar_lunes(semanas_mitad)

    def cambiar_estado(self, estado):
        if self.estado is not None:
            self.estado.delete()

        self.estado = estado
        self.estado_id = estado.pk
        self.save()

    def es_actualizable(self):
        return self.estado.es_actualizable()

    def es_adquirible(self):
        return self.estado.es_adquirible()

    def actualizar(self):
        self.estado.actualizar()

    def jueves(self):
        return self.fecha_inicio + timedelta(days=3)

    def fecha_fin(self):
        return self.fecha_inicio + timedelta(days=6)

    def fecha_abrir_subasta(self):
        lunes = self.fecha_inicio - timedelta(weeks=25)
        return lunes

    def fecha_cerrar_subasta(self):
        jueves = self.fecha_abrir_subasta() + timedelta(days=3)
        return jueves

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

    def esta_en_subasta(self):
        return self.estado.es_subasta()

    def establecer_comprador(self, nuevo_comprador):
        self.comprador = nuevo_comprador
        self.save()

    def __str__(self):
        return 'Semana {} con estado {}'.format(
            self.fecha_inicio, self.estado)

    class Meta:
        unique_together = ('content_type', 'estado_id')


class Estado(models.Model):

    semanas = GenericRelation(
        Semana,
        content_type_field='content_type',
        object_id_field='estado_id'
    )

    @classmethod
    def crear(cls, semana):
        if semana.estas_en_primer_mitad():
            estado = EnEspera.objects.create()
        else:
            estado = CompraDirecta.objects.create()
        semana.cambiar_estado(estado)

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

    def es_hotsale(self):
        return False

    def es_actualizable(self):
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

    def es_adquirible(self):
        return self.es_subasta() or \
            self.es_compra_directa() or \
            self.es_hotsale()

    def actualizar(self):
        pass

    # Modelo
    def __str__(self):
        raise NotImplementedError('Método abstracto, implementame')

    def get_absolute_url(self):
        return reverse(self.url(), args=[str(self.pk)])

    def url(self):
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
        return 'Ha pasado la fecha de ocupación de la semana'

    def get_absolute_url(self):
        return ''


class CompraDirecta(Estado):

    def __str__(self):
        return 'Compra directa'

    def es_compra_directa(self):
        return True

    def dar_de_baja(self):
        super().dar_de_baja()

    def abrir_subasta(self):
        precio_base = self.semana.residencia.precio_base
        subasta = Subasta.objects.create(precio_actual=precio_base)
        self.semana.cambiar_estado(subasta)
        return 'Se ha puesto la semana en subasta correctamente'

    def cerrar_subasta(self):
        pass

    def detalle(self):
        fecha_subasta = self.semana.fecha_abrir_subasta()
        return 'La semana entrará en subasta el día {}'.format(
            fecha_subasta.strftime("%A %d %B %Y - %H:%Mhs.")
        )

    def es_actualizable(self):
        lunes_espejo = date.today() + timedelta(weeks=25)
        return self.semana.fecha_inicio == lunes_espejo

    def actualizar(self):
        self.abrir_subasta()

    def url(self):
        return 'mostrar_compra_directa'


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

    def __str__(self):
        return 'Subasta'

    def es_subasta(self):
        return True

    def precio_minimo(self):
        return self.precio_actual + 0.1

    def nueva_puja(self, nuevo_pujador, nuevo_precio):
        if not self.el_ganador_es(nuevo_pujador):
            if self.ganador_actual:
                self.ganador_actual.incrementar_credito()
            self.semana.establecer_comprador(nuevo_pujador)
            nuevo_pujador.decrementar_credito()
        self.precio_actual = nuevo_precio
        self.save()

    def hay_ganador(self):
        return bool(self.ganador_actual)

    def el_ganador_es(self, usuario):
        return self.ganador_actual == usuario

    @property
    def ganador_actual(self):
        return self.semana.comprador

    def get_absolute_url(self):
        return reverse('mostrar_subasta', args=[str(self.pk)])

    def dar_de_baja(self):
        raise EventoNoPermitido('No se puede dar de baja una subasta activa')

    def abrir_subasta(self):
        pass

    def cerrar_subasta(self):
        if self.hay_ganador():
            reservada = Reservada.objects.create(
                precio_actual=self.precio_actual
            )
            self.semana.cambiar_estado(reservada)
        else:
            en_espera = EnEspera.objects.create()
            self.semana.cambiar_estado(en_espera)
        return 'Se ha cerrado la subasta correctamente'

    def detalle(self):
        fecha_cerrar_subasta = self.semana.fecha_cerrar_subasta()
        return 'La semana cerrará la subasta el día {}'.format(
            fecha_cerrar_subasta.strftime("%A %d %B %Y - %H:%Mhs.")
        )

    def es_actualizable(self):
        jueves_espejo = date.today() + timedelta(weeks=25)
        return self.semana.jueves() == jueves_espejo

    def actualizar(self):
        self.cerrar_subasta()

    def url(self):
        return 'mostrar_subasta'


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

    def establecer_hotsale(self, monto):
        hotsale = Hotsale.objects.create(precio_actual=monto)
        self.semana.cambiar_estado(hotsale)
        return hotsale

    def detalle(self):
        return 'Decida si poner en HotSale la semana'

    def es_actualizable(self):
        return self.semana.fecha_inicio == date.today()

    def actualizar(self):
        no_disponible = NoDisponible.objects.create()
        self.semana.cambiar_estado(no_disponible)

    def url(self):
        return 'mostrar_en_espera'


class Reservada(Estado):
    precio_actual = models.FloatField(
        null=True,
        blank=True
    )

    def __str__(self):
        return 'Reservada'

    def es_reservada(self):
        return True

    def actualizar(self):
        pass

    def dar_de_baja(self):
        raise EventoNoPermitido('La semana se encuentra reservada')

    def abrir_subasta(self):
        pass

    def cerrar_subasta(self):
        pass

    def detalle(self):
        return 'Semana reservada por {} {} con un monto de ${}'.format(
            self.semana.comprador.first_name,
            self.semana.comprador.last_name,
            self.precio_actual)

    def url(self):
        return 'mostrar_reservada'


class Hotsale(Estado):
    precio_actual = models.FloatField(
        null=True,
        blank=True
    )

    def __str__(self):
        return 'Hotsale'

    def abrir_subasta(self):
        pass

    def cerrar_subasta(self):
        pass

    def es_hotsale(self):
        return True

    def es_actualizable(self):
        return self.semana.fecha_inicio == date.today()

    def actualizar(self):
        no_disponible = NoDisponible.objects.create()
        self.semana.cambiar_estado(no_disponible)

    def detalle(self):
        return 'Semana en Hotsale por ${}'.format(self.precio_actual)

    def url(self):
        return 'mostrar_hotsale'
