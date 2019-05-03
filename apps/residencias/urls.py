from django.urls import path
from .views import AgregarResidenciaView

urlpatterns = [
    path('agregarResidencia.html',
         AgregarResidenciaView.as_view(),
         name='agregarResidencia'),
]
