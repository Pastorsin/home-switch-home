# Views
from django.views.generic import UpdateView, DetailView, ListView
# Models
from django.contrib.auth.models import User
from adquisiciones.models import CompraDirecta, Subasta, NoDisponible
from .models import Residencia
# Forms
from .forms import ResidenciaForm, UbicacionForm
# Utility Django
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.utils.text import camel_case_to_spaces as humanize
# Utility python
from datetime import date, timedelta
import json


class AgregarResidenciaView(UpdateView):
    template_name = 'agregarResidencia.html'
    form_class = ResidenciaForm
    ubicacion_form_class = UbicacionForm

    def get_context_data(self, **kwargs):
        context = super(AgregarResidenciaView, self).get_context_data(**kwargs)
        if 'residencia' not in context:
            context['residencia'] = self.form_class()
        if 'ubicacion' not in context:
            context['ubicacion'] = self.ubicacion_form_class()
        return context

    def get_object(self):
        return get_object_or_404(User)

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        residencia_form = self.form_class(request.POST)
        ubicacion_form = self.ubicacion_form_class(request.POST)
        if self.formulario_es_valido(residencia_form, ubicacion_form):
            self.guardar_formulario(residencia_form, ubicacion_form)
            messages.success(self.request, 'Residencia agregada exitosamente!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            error = 'Error! Ya existe otra residencia con la misma ubicación'
            messages.error(self.request, error)
            context = self.get_context_data(residencia=residencia_form,
                                            ubicacion=ubicacion_form)
            return self.render_to_response(context)

    def formulario_es_valido(self, residencia_form, ubicacion_form):
        return residencia_form.is_valid() and ubicacion_form.is_valid()

    def guardar_formulario(self, residencia_form, ubicacion_form):
        ubicacion_data = self.guardar_ubicacion(ubicacion_form)
        estado_data = self.guardar_estado()
        self.guardar_residencia(ubicacion_data, estado_data, residencia_form)

    def guardar_ubicacion(self, ubicacion_form):
        ubicacion_data = ubicacion_form.save(commit=False)
        ubicacion_data.save()
        return ubicacion_data

    def guardar_estado(self):
        estado_data = CompraDirecta()
        estado_data.save()
        return estado_data

    def guardar_residencia(self, ubicacion_data, estado_data, residencia_form):
        residencia_data = residencia_form.save(commit=False)
        residencia_data.ubicacion = ubicacion_data
        residencia_data.estado = estado_data
        residencia_data.estado_id = estado_data.id
        residencia_data.save()

    def get_success_url(self):
        return reverse('agregarResidencia')


class ModificarResidenciaView(UpdateView):

    model = Residencia
    template_name = 'modificarResidencia.html'
    form_class = ResidenciaForm
    ubicacion_form_class = UbicacionForm

    def get_context_data(self, **kwargs):
        context = super(ModificarResidenciaView,
                        self).get_context_data(**kwargs)
        context['ubicacion'] = self.ubicacion_form_class(instance=context['residencia'].ubicacion)
        return context

    def post(self, request, *args, **kwargs):
        residencia=self.get_object()
        if residencia.estado.es_subasta():
            error='Error! No se ha podido modificar la residencia. Actualmente se encuentra en subasta.'    
            messages.error(self.request, error)
            return HttpResponseRedirect(residencia.get_absolute_url())
        ubicacion_form = UbicacionForm(request.POST, instance=residencia.ubicacion)
        form = ResidenciaForm(request.POST, instance=residencia)          
        if self.formulario_es_valido(form,ubicacion_form):    
            ubicacion_form.save()
            form.save()
            messages.success(self.request, 'Residencia modificada exitosamente!')
        else:
            error='Error! No se puede modificar porque la ubicacion ya existe para otra residencia.'
            messages.error(self.request,error)
        return HttpResponseRedirect(residencia.get_absolute_url())

    def formulario_es_valido(self, residencia_form, ubicacion_form):
        return residencia_form.is_valid() and ubicacion_form.is_valid()  


class ListadoResidenciasView(ListView):
    template_name = 'listadoResidencias.html'
    model = Residencia
    objetos = model.objects.order_by('precio_base')


class Accion():

    def __init__(self, residencia):
        self.residencia = residencia

    def exito(self):
        raise Exception('Método abstracto, implementame')

    def estado(self):
        raise Exception('Método abstracto, implementame')

    def mensaje_exito(self):
        raise Exception('Método abstracto, implementame')

    def mensaje_error(self):
        raise Exception('Método abstracto, implementame')


class AccionAbrirSubasta(Accion):

    SEMANAS_MINIMAS = 26  # 6 meses = 26 semanas

    def exito(self):
        # tiempo_transcurrido = date.today() - residencia.fecha_publicacion
        # tiempo_transcurrido >= timedelta(weeks=self.SEMANAS_MINIMAS)
        return True

    def mensaje_error(self):
        return 'La residencia debe estar como minimo 6 meses en compra directa'

    def estado(self):
        return Subasta

    def mensaje_exito(self):
        return 'Se ha puesto la residencia en {} correctamente'.format(
            humanize(self.estado().__name__))


class AccionCerrarSubasta(AccionAbrirSubasta):

    def estado(self):
        return CompraDirecta


class AccionEliminar(Accion):

    def exito(self):
        return True

    def mensaje_error(self):
        return 'No se pudo eliminar la residencia'

    def estado(self):
        return NoDisponible

    def mensaje_exito(self):
        return 'Se ha eliminado la residencia correctamente'


class MostrarResidenciaView(DetailView):

    model = Residencia
    template_name = 'detalle_residencia.html'
    acciones = {
        'abrir_subasta': AccionAbrirSubasta,
        'eliminar': AccionEliminar,
        'cerrar_subasta': AccionCerrarSubasta
    }

    def se_presiono_algun_boton(self, request):
        return bool(self.boton_presionado(request))

    def boton_presionado(self, request):
        for nombre_boton in self.acciones:
            if nombre_boton in request.POST.keys():
                return nombre_boton

    def post(self, request, *args, **kwargs):
        residencia = self.get_object()
        if self.se_presiono_algun_boton(request):
            boton_presionado = self.boton_presionado(request)
            accion = self.acciones[boton_presionado]()
            if accion.exito():
                residencia.cambiar_estado(accion.estado())
                messages.success(self.request, accion.mensaje_exito())
            else:
                messages.error(self.request, accion.mensaje_error())
            return HttpResponseRedirect(residencia.get_absolute_url())
        else:
            raise Exception('No se presionó ningún botón y entró acá')
