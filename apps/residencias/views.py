# Views
from django.views.generic import UpdateView, DetailView, ListView, CreateView
# Models
from django.db.models import Q
from accounts.models import CustomUser
from adquisiciones.models import EventoNoPermitido
from .models import Residencia
from adquisiciones.models import Semana
# Forms
from .forms import ResidenciaForm, UbicacionForm, BusquedaResidenciaForm
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
            exito = 'Residencia agregada exitosamente!'
            messages.success(self.request, exito)
            return HttpResponseRedirect(self.get_success_url())
        else:
            error = 'Error! Ya existe otra residencia con la misma ubicación'
            messages.error(self.request, error)

            context = self.get_context_data(
                residencia=residencia_form, ubicacion=ubicacion_form)
            return self.render_to_response(context)

    def formulario_es_valido(self, residencia_form, ubicacion_form):
        return residencia_form.is_valid() and ubicacion_form.is_valid()

    def guardar_formulario(self, residencia_form, ubicacion_form):
        ubicacion_data = self.guardar_ubicacion(ubicacion_form)
        self.guardar_residencia(ubicacion_data, residencia_form)

    def guardar_ubicacion(self, ubicacion_form):
        ubicacion_data = ubicacion_form.save(commit=False)
        ubicacion_data.save()
        return ubicacion_data

    def guardar_residencia(self, ubicacion_data, residencia_form):
        residencia_data = residencia_form.save(commit=False)
        residencia_data.ubicacion = ubicacion_data
        residencia_data.save()
        residencia_data.crear_semanas()

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
        if 'ubicacion' not in context:
            context['ubicacion'] = self.ubicacion_form_class(
                instance=context['residencia'].ubicacion)
        return context

    def post(self, request, *args, **kwargs):
        residencia = self.get_object()
        self.object = self.get_object()
        if residencia.esta_en_subasta():
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
            context = self.get_context_data(residencia=form,
                                            ubicacion=ubicacion_form)
            return self.render_to_response(context)
        return HttpResponseRedirect(residencia.get_absolute_url())

    def formulario_es_valido(self, residencia_form, ubicacion_form):
        return residencia_form.is_valid() and ubicacion_form.is_valid()


class ListadoResidenciasView(ListView):
    template_name = 'listadoResidencias.html'
    model = Residencia
    form_class = BusquedaResidenciaForm
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ListadoResidenciasView,
                        self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        busqueda = self.form_class(request.POST)
        if busqueda.is_valid():
            self.object_list = self.get_query_set(busqueda.data)
        else:
            self.object_list = self.model.objects.all()
        context = self.get_context_data(form=busqueda)
        return self.render_to_response(context)

    def get_query_set(self, busqueda):
        pais = busqueda['pais']
        provincia = busqueda['provincia']
        ciudad = busqueda['ciudad']
        fecha_inicio = busqueda['fecha_inicio']
        fecha_hasta = busqueda['fecha_hasta']
        if not fecha_inicio or not fecha_hasta:
            semanas = Semana.objects.all()
        else:
            semanas = Semana.objects.filter(
                (Q(content_type__model='compradirecta') |
                 Q(content_type__model='subasta') |
                 Q(content_type__model='hotsale')) &
                Q(fecha_inicio__range=[fecha_inicio, fecha_hasta])
            )
        return Residencia.objects.filter(
            ubicacion__pais__startswith=pais,
            ubicacion__provincia__startswith=provincia,
            ubicacion__ciudad__startswith=ciudad,
            semana__in=semanas).distinct()


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
            'eliminar': self.residencia.eliminar
        }

    def post(self, request, *args, **kwargs):
        self.inicializar_eventos()
        evento = self.eventos[self.boton_presionado(request)]
        try:
            mensaje_exito = evento()
            self.residencia.save()
            messages.success(self.request, mensaje_exito)
        except EventoNoPermitido as mensaje_error:
            messages.error(self.request, mensaje_error)
        return HttpResponseRedirect(self.residencia.get_absolute_url())
