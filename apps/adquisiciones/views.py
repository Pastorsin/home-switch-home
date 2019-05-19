from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from .models import Subasta
from django.contrib import messages

# Create your views here.


class MostrarSubastaView(DetailView):

    model = Subasta
    template_name = 'mostrar_subasta.html'

    def post(self, request, *args, **kwargs):
        subasta = self.get_object()

        # if usuario_conectado.tiene_creditos():
        if True:
            usuario_conectado = request.user
            nuevo_monto = request.POST['monto']
            subasta.nueva_puja(usuario_conectado, nuevo_monto)
            mensaje_exito = 'Puja realizada con éxito!'
            messages.success(request, mensaje_exito)
        else:
            mensaje_error = 'Error! No tenés créditos suficientes para pujar'
            messages.error(request, mensaje_error)
        return HttpResponseRedirect(subasta.get_absolute_url())
