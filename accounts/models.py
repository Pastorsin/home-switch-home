# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
import datetime
from datetime import date


class Banco(models.Model):
    nombre = models.CharField(
        max_length=255,
        unique=True
    )
    foto = models.URLField()

    def __str__(self):
        return self.nombre


class Tarjeta(models.Model):
    numero = models.CharField(
        verbose_name='Número de tarjeta',
        max_length=255
    )
    nombre_completo = models.CharField(
        max_length=255,
    )
    fecha_vencimiento = models.CharField(
        verbose_name='Fecha de vencimiento',
        max_length=10,
    )
    cvc = models.CharField(
        verbose_name='CVC (Código de seguridad)',
        max_length=4
    )
    banco = models.ForeignKey(
        Banco,
        related_name='banco',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return 'Tarjeta de {}'.format(self.nombre_completo)


class CustomUser(AbstractUser):
    """
    Reúne las cualidades de los usuarios comúnes y
    el manejo de usuarios en genericos.
    Las subclases de esta clase deberian ser consideradas como 'perfiles' que
    especializan esta clase para un tipo determinado de usuario
    """
    email = models.EmailField(
        unique=True
    )
    username = models.CharField(
        max_length=150,
        unique=False    # Ahora el mail es unico
    )

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    def nombre_completo(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def eliminar(self):
        self.is_active = False
        self.save()
        return 'Se ha eliminado al usuario exitosamente'

    def get_absolute_url(self):
        return reverse('verPerfil', args=[str(self.pk)])

    def notificaciones(self):
        from adquisiciones.models import Notificacion
        return Notificacion.objects.filter(usuario=self)

    def agregar_notificacion(self, mensaje, semana):
        from adquisiciones.models import Notificacion
        if not self.tengo_notificacion(mensaje, semana):
            Notificacion.objects.create(
                mensaje=mensaje,
                semana=semana,
                usuario=self
            )

    def notificaciones_sin_leer(self):
        return self.notificaciones().filter(leida=False)

    def leer_notificaciones(self):
        self.notificaciones_sin_leer().update(leida=True)

    def tiene_notificaciones_sin_leer(self):
        return self.notificaciones_sin_leer().exists()

    def eliminar_notificacion(self, mensaje):
        self.notificaciones().filter(
            mensaje=mensaje).delete()

    def tengo_notificacion(self, mensaje, semana):
        return self.notificaciones().filter(
            mensaje=mensaje,
            semana__residencia=semana.residencia).exists()


class Admin(models.Model):
    # Clase destinada a preveer algún tipo de método o
    # cualidad especifica de admin
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True
    )

    def nombre_c(self):
        return self.user.nombre_completo()


class UsuarioEstandar(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True
    )
    fecha_nacimiento = models.DateField(
        help_text='Debe ser mayor de 18 años para poder reservar!',
        null=True,
    )
    foto = models.URLField(
        help_text='** Campo opcional',
        null=True,
        blank=True
    )
    es_premium = models.BooleanField(
        default=False
    )
    creditos = models.PositiveIntegerField(
        null=True,
        default=2
    )
    dni = models.CharField(
        help_text='Ingrese los digitos sin separadores \
        ni espacios por favor. Ej: 11222333',
        max_length=8,
        null=True,
    )
    tarjeta = models.OneToOneField(
        Tarjeta,
        on_delete=models.CASCADE,
        null=True
    )
    fecha_creacion = models.DateField(
        default=datetime.date.today
    )

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def semanas_seguidas(self):
        """Retorna las semanas seguidas por el usuario"""
        from adquisiciones.models import Semana
        return Semana.objects.filter(seguidores__pk=self.pk)

    def cambiar_categoria(self):
        self.es_premium = not self.es_premium
        self.save()

    def __str__(self):
        return self.user.email

    def edad(self):
        today = date.today()
        return today.year - self.fecha_nacimiento.year - \
            ((today.month, today.day) <
             (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

    def tenes_creditos(self):
        return self.creditos > 0

    def decrementar_credito(self):
        self.creditos -= 1
        self.save()

    def incrementar_credito(self):
        self.creditos += 1
        self.save()
