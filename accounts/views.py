from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import CustomUserCreationForm
from .models import CustomUser


class SignUpView(CreateView):

    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class DetallePerfilView(DetailView):
    model = CustomUser
    template_name = 'verPerfil.html'
