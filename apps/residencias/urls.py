from django.urls import path
from .views import AgregarResidenciaView, MostrarResidenciaView

urlpatterns = [
    path('agregarResidencia.html', AgregarResidenciaView.as_view(), name='agregarResidencia'),
    path('residencia/<int:pk>/', MostrarResidenciaView.as_view(), name='detalle_residencia'),
]
