from .forms import ResidenciaForm
from django.views.generic.edit import FormView

# Create your views here.


class AgregarResidenciaView(FormView):

    template_name = 'agregarResidencia.html'
    form_class = ResidenciaForm
