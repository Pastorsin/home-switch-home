# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    fecha_nacimiento = models.DateField(
        null=True,
        blank=True
    )
    foto = models.URLField(
        null=True,
        blank=True
    )
    es_premium = models.BooleanField(
        default=False
    )
    creditos = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=2
    )
    email = models.EmailField(
        unique=True
    )
    username = models.CharField(
        max_length=150,
        unique=False    # Ahora el mail es unico
    )
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

