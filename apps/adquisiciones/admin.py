from django.contrib import admin
from .models import CompraDirecta, Subasta, Semana, EnEspera, NoDisponible

admin.site.register(CompraDirecta)
admin.site.register(Subasta)
admin.site.register(Semana)
admin.site.register(EnEspera)
admin.site.register(NoDisponible)
