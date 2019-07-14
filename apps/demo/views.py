from django.views.generic import TemplateView
import os
from datetime import date, timedelta

from django.views.generic import TemplateView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout

from accounts.models import CustomUser
from residencias.models import Residencia
from adquisiciones.models import Notificacion


def _deshabilitar_hora_automatica():
    os.system('sudo timedatectl set-ntp false')


def _habilitar_hora_automatica():
    os.system('sudo timedatectl set-ntp true')


def _establecer_fecha(fecha):
    _deshabilitar_hora_automatica()
    os.system('sudo date -s "{}"'.format(fecha.strftime("%Y%m%d")))


def establecer_lunes():
    lunes = date.today() - timedelta(days=date.today().weekday())
    _establecer_fecha(lunes)


def establecer_jueves():
    jueves = date.today() + timedelta(days=3 - date.today().weekday())
    _establecer_fecha(jueves)


def incrementar_semana():
    _establecer_fecha(date.today() + timedelta(weeks=1))


def decrementar_semana():
    _establecer_fecha(date.today() - timedelta(weeks=1))


def cerrar_subasta():
    Notificacion.objects.all().delete()
    for residencia in Residencia.objects.all():
        residencia.actualizar()


def abrir_subasta():
    Notificacion.objects.all().delete()
    for residencia in Residencia.objects.all():
        residencia.actualizar()
        residencia.crear_nueva_semana()


def ir_lejos():
    _establecer_fecha(date.today() + timedelta(days=365))


class DemoView(TemplateView):
    template_name = 'demo.html'

    def post(self, request, *args, **kwargs):
        if 'lunes' in request.POST.keys():
            incrementar_semana()
            establecer_lunes()
            abrir_subasta()
        elif 'jueves' in request.POST.keys():
            establecer_jueves()
            cerrar_subasta()
        elif 'lejos' in request.POST.keys():
            ir_lejos()
        elif 'reiniciar' in request.POST.keys():
            _habilitar_hora_automatica()
        return HttpResponseRedirect(reverse('demo'))
