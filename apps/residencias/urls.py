from django.urls import path
from .views import AgregarResidenciaView
from .views import ListadoResidenciasView
from .views import MostrarResidenciaView

urlpatterns = [
    path('agregarResidencia',
         AgregarResidenciaView.as_view(),
         name='agregarResidencia'),
    path('listadoResidencias',
         ListadoResidenciasView.as_view(),
         name='listadoResidencias'),
    path('residencia/<int:pk>/',
         MostrarResidenciaView.as_view(),
         name='detalle_residencia')
]
