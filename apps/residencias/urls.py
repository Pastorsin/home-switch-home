from django.urls import path
from .views import AgregarResidenciaView
from .views import ListadoResidenciasView
from .views import MostrarResidenciaView
from .views import ModificarResidenciaView

urlpatterns = [
    path('agregarResidencia',
         AgregarResidenciaView.as_view(),
         name='agregarResidencia'),
    path('listadoResidencias',
         ListadoResidenciasView.as_view(),
         name='listadoResidencias'),
    path('residencia/<int:pk>/',
         MostrarResidenciaView.as_view(),
         name='detalle_residencia'),
    path('modificarResidencia/<int:pk>/',
         ModificarResidenciaView.as_view(),
         name='modificarResidencia')
]
