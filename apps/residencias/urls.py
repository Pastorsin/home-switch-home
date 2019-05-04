from django.urls import path
from .views import AgregarResidenciaView
from .views import ListadoResidenciasView

urlpatterns = [
    path('agregarResidencia.html',
         AgregarResidenciaView.as_view(),
         name='agregarResidencia'),
    path('listadoResidencias.html',
    	ListadoResidenciasView.as_view(),
    	name='listadoResidencias'),
]
