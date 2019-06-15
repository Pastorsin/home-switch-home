from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DetailView

from .forms import CustomUserCreationForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class DetallePerfilView(DetailView):
    model = CustomUser
    template_name = 'verPerfil.html'


class EditProfileView(UpdateView):
    model = CustomUser
    template_name = 'user_edit.html'
    fields = ('first_name', 'last_name', 'email', 'foto', 'fecha_nacimiento', 'dni')
    success_url = reverse_lazy('home')
