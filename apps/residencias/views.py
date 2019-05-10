# Views
from django.views.generic import UpdateView, DetailView
# Models
from django.contrib.auth.models import User
from .models import Residencia
from adquisiciones.models import CompraDirecta
# Forms
from .forms import ResidenciaForm, UbicacionForm
# Utility
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.views.generic import ListView


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


class ListadoResidenciasView(ListView):
    template_name = 'listadoResidencias.html'
    model = Residencia
    objetos = model.objects.order_by('precio_base')


class MostrarResidenciaView(DetailView):

    model = Residencia
    template_name = 'detalle_residencia.html'
