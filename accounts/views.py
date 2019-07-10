from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .forms import TarjetaForm, AdminCreationForm, PublicUserChangeForm
from .models import CustomUser, Tarjeta
from adquisiciones.models import Semana


class UserSignUpView(CreateView):
    form_class = CustomUserCreationForm
    tarjeta_form_class = TarjetaForm
    success_url = reverse_lazy('login')
    template_name = 'user_signup.html'

    def get_context_data(self, **kwargs):
        context = super(UserSignUpView, self).get_context_data(**kwargs)
        if 'usuario' not in context:
            context['usuario'] = self.form_class()
        if 'tarjeta' not in context:
            context['tarjeta'] = self.tarjeta_form_class()
        return context

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        # Usuario anónimo
        self.object = None

        user_form = self.form_class(request.POST)
        tarjeta_form = self.tarjeta_form_class(request.POST)

        if user_form.is_valid() and tarjeta_form.is_valid():
            self.guardar_formulario(user_form, tarjeta_form)
            return HttpResponseRedirect(self.success_url)
        else:
            context = self.get_context_data(
                usuario=user_form, tarjeta=tarjeta_form)
            return self.render_to_response(context)

    def guardar_formulario(self, user_form, tarjeta_form):
        tarjeta_data = tarjeta_form.save()
        user_data = user_form.save(commit=False)
        user_data.usuarioestandar.tarjeta = tarjeta_data
        user_data.usuarioestandar.save()
        user_data.save()


class DetallePerfilView(DetailView):
    model = CustomUser
    template_name = 'verPerfil.html'


class EditProfileView(UpdateView):
    form_class = CustomUserChangeForm
    form_estandar = PublicUserChangeForm
    model = CustomUser
    template_name = 'user_edit.html'

    def get_context_data(self, **kwargs):
        context = super(EditProfileView, self).get_context_data(**kwargs)
        if 'estandar' not in context:
            usuario = context['customuser']
            context['estandar'] = self.form_estandar(
                instance=usuario.usuarioestandar
            )
        return context

    def post(self, request, *args, **kwargs):
        usuario = self.object = self.get_object()
        usuario_form = self.form_class(
            request.POST,
            instance=usuario
        )
        estandar_form = self.form_estandar(
            request.POST,
            instance=usuario.usuarioestandar
        )
        context = self.get_context_data(
            customuser=usuario_form,
            estandar=estandar_form
        )
        return self.__procesar_form(usuario_form, estandar_form, context)

    def __procesar_form(self, usuario_form, estandar_form, context):
        if self.__form_valido(usuario_form, estandar_form):
            self.__guardar(usuario_form, estandar_form)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(context)

    def __form_valido(self, usuario_form, estandar_form):
        return usuario_form.is_valid() and estandar_form.is_valid()

    def __guardar(self, usuario_form, estandar_form):
        usuario_form.save()
        estandar_form.save()

    def get_success_url(self):
        return reverse_lazy('verPerfil', args=[str(self.request.user.pk)])


class EditarTarjetaView(UpdateView):
    model = Tarjeta
    template_name = 'editar_tarjeta.html'
    form_class = TarjetaForm

    def get_success_url(self):
        return reverse_lazy('verPerfil', args=[str(self.request.user.pk)])


class MisReservasView(ListView):
    model = Semana
    template_name = 'mis_reservas.html'

    def get_queryset(self):
        usuario = self.request.user
        return Semana.objects.filter(
            content_type__model='reservada',
            comprador=usuario
        )


class MisSubastasView(ListView):
    model = Semana
    template_name = 'mis_subastas.html'

    def get_queryset(self):
        usuario = self.request.user
        return Semana.objects.filter(
            content_type__model='subasta',
            comprador=usuario
        )


class AdminSignUpView(SuccessMessageMixin, CreateView):
    form_class = AdminCreationForm
    success_url = reverse_lazy('admin_signup')
    template_name = 'admin_signup.html'
    success_message = 'Administrador creado correctamente'
