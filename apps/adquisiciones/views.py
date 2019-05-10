from django.views.generic import DetailView
from .models import Subasta

# Create your views here.


class MostrarSubastaView(DetailView):

    model = Subasta
    template_name = 'mostrar_subasta.html'
