from django.urls import path
from .views import MostrarSubastaView, SemanasView

urlpatterns = [
    path('subasta/<int:pk>/',
         MostrarSubastaView.as_view(),
         name='mostrar_subasta'),
    path('residencia/<int:pk>/semanas',
         SemanasView.as_view(),
         name='listado_semanas')
]
