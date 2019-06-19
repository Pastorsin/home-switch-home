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
    email = models.EmailField(
        unique=True
    )
    username = models.CharField(
        max_length=150,
        unique=False    # Ahora el mail es unico
    )
    fecha_creacion = models.DateField(
        default=datetime.date.today)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    @property
    def semanas_seguidas(self):
        """Retorna las semanas seguidas por el usuario"""
        return self.seguidores.all()

    @property
    def reservas_del_año(self):
        """Retorna las semanas compradas por el usuario"""
        return self.comprador.all()    # TODO probablemente haya que filtrar las del año actual

    def cambiar_categoria(self):
        self.es_premium = not self.es_premium
        self.save()

    def __str__(self):
        return 'Usuario {} {} con creditos: {}'.format(
            self.first_name, self.last_name, self.creditos)

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

    def get_absolute_url(self):
        return reverse('verPerfil', args=[str(self.pk)])
