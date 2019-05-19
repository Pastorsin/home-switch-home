# Views
from django.views.generic import UpdateView, DetailView, ListView, CreateView
# Models
from accounts.models import CustomUser
from adquisiciones.models import CompraDirecta
from adquisiciones.models import EventoNoPermitido
from .models import Residencia
# Forms
from .forms import ResidenciaForm, UbicacionForm
# Utility Django
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404
# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin


class AgregarResidenciaView(LoginRequiredMixin, CreateView):
    template_name = 'agregarResidencia.html'
    form_class = ResidenciaForm
    ubicacion_form_class = UbicacionForm
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(AgregarResidenciaView, self).get_context_data(**kwargs)
        if 'residencia' not in context:
            context['residencia'] = self.form_class()
        if 'ubicacion' not in context:
            context['ubicacion'] = self.ubicacion_form_class()
        return context

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_object(self, request):
        return get_object_or_404(CustomUser, pk=request.user.pk)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(request)
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


class ModificarResidenciaView(LoginRequiredMixin, UpdateView):

    model = Residencia
    template_name = 'modificarResidencia.html'
    form_class = ResidenciaForm
    ubicacion_form_class = UbicacionForm
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(ModificarResidenciaView,
                        self).get_context_data(**kwargs)
        context['ubicacion'] = self.ubicacion_form_class(
            instance=context['residencia'].ubicacion)
        return context

    def post(self, request, *args, **kwargs):
        residencia = self.get_object()
        if residencia.estado.es_subasta():
            error = 'Error! No se ha podido modificar la residencia. ' + \
                'Actualmente se encuentra en subasta.'
            messages.error(self.request, error)
            return HttpResponseRedirect(residencia.get_absolute_url())
        ubicacion_form = UbicacionForm(
            request.POST, instance=residencia.ubicacion)
        form = ResidenciaForm(request.POST, instance=residencia)
        if self.formulario_es_valido(form, ubicacion_form):
            ubicacion_form.save()
            form.save()
            messages.success(
                self.request, 'Residencia modificada exitosamente!')
        else:
            error = 'Error! No se puede modificar porque la ubicación ' + \
                'ya existe para otra residencia.'
            messages.error(self.request, error)
        return HttpResponseRedirect(residencia.get_absolute_url())

    def formulario_es_valido(self, residencia_form, ubicacion_form):
        return residencia_form.is_valid() and ubicacion_form.is_valid()


class ListadoResidenciasView(ListView):
    template_name = 'listadoResidencias.html'
    model = Residencia
    objetos = model.objects.order_by('precio_base')


class MostrarResidenciaView(DetailView):

    model = Residencia
    template_name = 'detalle_residencia.html'

    def boton_presionado(self, request):
        for nombre_boton in self.eventos:
            if nombre_boton in request.POST.keys():
                return nombre_boton

    def inicializar_eventos(self):
        self.residencia = self.get_object()
        self.eventos = {
            'abrir_subasta': self.residencia.abrir_subasta,
            'eliminar': self.residencia.eliminar,
            'cerrar_subasta': self.residencia.cerrar_subasta,
            'hotsale': self.residencia.establecer_hotsale,
            'comprar': self.residencia.comprar
        }

    def post(self, request, *args, **kwargs):
        self.inicializar_eventos()
        evento = self.eventos[self.boton_presionado(request)]
        try:
            mensaje_exito = evento()
            messages.success(self.request, mensaje_exito)
        except EventoNoPermitido as mensaje_error:
            messages.error(self.request, mensaje_error)
        return HttpResponseRedirect(self.residencia.get_absolute_url())


