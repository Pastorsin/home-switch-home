from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    edad = models.PositiveIntegerField(
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

    def cambiar_categoria(self):
        if self.es_premium:
            self.es_premium = False
        else:
            self.es_premium = True
        self.save()
