from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import ResidenciaForm, UbicacionForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from .models import Residencia


class AgregarResidenciaView(UpdateView):
    template_name = 'agregarResidencia.html'
    form_class = ResidenciaForm
    second_form_class = UbicacionForm

    def get_context_data(self, **kwargs):
        context = super(AgregarResidenciaView, self).get_context_data(**kwargs)
        if 'residencia' not in context:
            context['residencia'] = self.form_class()
        if 'ubicacion' not in context:
            context['ubicacion'] = self.second_form_class()
        return context

    def get_object(self):
        return get_object_or_404(User)

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)

        if form.is_valid() and form2.is_valid():
            ubicacion_data = form2.save(commit=False)
            ubicacion_data.save()
            residencia_data = form.save(commit=False)
            residencia_data.ubicacion = ubicacion_data
            residencia_data.save()
            messages.success(self.request, 'Residencia agregada exitosamente!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form, form2=form2))

    def get_success_url(self):
        return reverse('agregarResidencia')


class ListadoResidenciasView(ListView):
    template_name = 'listadoResidencias.html'
    model = Residencia
    objetos = model.objects.order_by('precio_base')
    """context_object_name = 'residencias'"""