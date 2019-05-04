from django.urls import path
<<<<<<< HEAD
from .views import AgregarResidenciaView
from .views import ListadoResidenciasView

urlpatterns = [
    path('agregarResidencia.html',
         AgregarResidenciaView.as_view(),
         name='agregarResidencia'),
    path('listadoResidencias.html',
    	ListadoResidenciasView.as_view(),
    	name='listadoResidencias'),
=======
from .views import AgregarResidenciaView, MostrarResidenciaView

urlpatterns = [
    path('agregarResidencia.html', AgregarResidenciaView.as_view(), name='agregarResidencia'),
    path('residencia/<int:pk>/', MostrarResidenciaView.as_view(), name='detalle_residencia'),
>>>>>>> 9ef629c4b2c2efb1b4638a7d3ab7b844f785e2cd
]
